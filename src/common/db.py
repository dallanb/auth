import collections
import re

import inflect
from sqlalchemy import inspect, or_, and_

from .. import db
from ..common.cleaner import Cleaner
from ..common.error import *


class DB:
    # Helpers
    @classmethod
    def _query_builder(cls, model, filters=[], expand=[], include=[], sort_by=None, limit=None, offset=None):
        query = db.session.query(model)
        for logic_operator, filter_arr in filters:
            criterion = []
            for key, value in filter_arr:
                if key == 'like':
                    for like_k, like_v in value:
                        search = "%{}%".format(like_v)
                        criterion.append(like_k.like(search))
                if key == 'equal':
                    for equal_k, equal_v in value:
                        criterion.append(equal_k == equal_v)
                if key == 'gt':
                    for gt_k, gt_v in value:
                        criterion.append(gt_k > gt_v)
                if key == 'gte':
                    for gte_k, gte_v in value:
                        criterion.append(gte_k >= gte_v)
                if key == 'lt':
                    for lt_k, lt_v in value:
                        criterion.append(lt_k < lt_v)
                if key == 'lte':
                    for lte_k, lte_v in value:
                        criterion.append(lte_k <= lte_v)
                if key == 'in':
                    for in_k, in_v in value:
                        criterion.append(in_k.in_(in_v))
                if key == 'has_key':
                    for has_key_k, has_key_v in value:
                        criterion.append(has_key_k.has_key(has_key_v))
            if logic_operator == 'or':
                query = query.filter(or_(*criterion))
            if logic_operator == 'and':
                query = query.filter(and_(*criterion))
        for i, k in enumerate(expand):
            tables = k.split('.')
            options = db.lazyload(getattr(model, tables[0]))
            for j, table in enumerate(tables):
                if j > 0:
                    nested_class = cls._get_class_by_tablename(tables[j - 1])
                    options = options.lazyload(getattr(nested_class, table))
            query = query.options(options)
        for i, k in enumerate(include):
            tables = k.split('.')
            options = db.joinedload(getattr(model, tables[0]))
            for j, table in enumerate(tables):
                if j > 0:
                    nested_class = cls._get_class_by_tablename(cls._singularize(tables[j - 1]))
                    options = options.joinedload(getattr(nested_class, table))
            query = query.options(options)
        if sort_by is not None:
            direction = re.search('[.](a|de)sc', sort_by)
            if direction is not None:
                direction = direction.group()
            key = sort_by.split(direction)[0]
            if direction == '.asc':
                query = query.order_by(getattr(model, key).asc())
            elif direction == '.desc':
                query = query.order_by(getattr(model, key).desc())
            else:  # for now, lack of a direction will be interpreted as asc
                query = query.order_by(getattr(model, key).asc())
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query

    @classmethod
    def _get_class_by_tablename(cls, tablename):
        for c in db.Model._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
                return c

    @classmethod
    def _is_pending(cls, instance):
        inspection = inspect(instance)
        return inspection.pending

    @classmethod
    def _get_cache_key(cls, model, query):
        return f"{model.__tablename__}:{str(query)}"

    @classmethod
    def _pluralize(cls, tablename):
        p = inflect.engine()
        return p.plural_noun(tablename)

    @classmethod
    def _singularize(cls, tablename):
        p = inflect.engine()
        return p.singular_noun(tablename)

    @classmethod
    def _generate_equal_filter(cls, model, **kwargs):
        equal_filter = []
        for k, v in kwargs.items():
            equal_filter.append(
                (
                    'and',
                    [
                        ('equal', [(getattr(model, k), v)])
                    ]
                )
            )
        return equal_filter

    @classmethod
    def _generate_nested_filter(cls, nested):
        nested_filter = []
        for k, v in nested.items():
            nested_class = cls._get_class_by_tablename(k)
            for nested_k, nested_v in v.items():
                nested_filter.append(
                    (
                        'and',
                        [
                            ('equal', [(getattr(nested_class, nested_k), nested_v)])
                        ]
                    )
                )
        return nested_filter

    @classmethod
    def _generate_search_filter(cls, model, search):
        search_filter = []
        if 'key' in search:
            search_filter.append(
                (
                    'or',
                    [
                        (
                            'like',
                            [
                                (getattr(model, field), search['key'])
                            ]
                        ) for field in search['fields']
                    ]
                )
            )
        return search_filter

    @classmethod
    def _generate_in_filter(cls, model, within):
        in_filter = []
        for k, v in within.items():
            in_filter.append(
                (
                    'and',
                    [
                        ('in', [(getattr(model, k), v)])
                    ]
                )
            )
        return in_filter

    @classmethod
    def _generate_has_key_filter(cls, model, has_key):
        has_key_filter = []
        for k, v in has_key.items():
            has_key_filter.append(
                (
                    'and',
                    [
                        ('has_key', [(getattr(model, k), v)])
                    ]
                )
            )

        return has_key_filter

    @classmethod
    def _generate_filters(cls, model, nested=None, search=None, within=None, has_key=None, **kwargs):
        filters = []

        if len(kwargs):
            filters.extend(cls._generate_equal_filter(model=model, **kwargs))

        if nested:
            filters.extend(cls._generate_nested_filter(nested=nested))

        if search:
            filters.extend(cls._generate_search_filter(model=model, search=search))

        if within:
            filters.extend(cls._generate_in_filter(model=model, within=within))

        if has_key:
            filters.extend(cls._generate_has_key_filter(model=model, has_key=has_key))

        return filters

    # Methods
    @classmethod
    def init(cls, model, **kwargs):
        return model(**kwargs)

    @classmethod
    def count(cls, model):
        return db.session.query(model).count()

    @classmethod
    def save(cls, instance):
        if not instance:
            raise MissingParamError(instance.__tablename__)
        if not Cleaner.is_mapped(instance):
            raise InvalidTypeError(instance.__tablename__, 'mapped')

        if not cls._is_pending(instance):
            db.session.add(instance)

        db.session.commit()
        return instance

    @classmethod
    # TODO: Consider using dataclass instead of a named tuple
    def find(cls, model, page=None, per_page=None, expand=[], include=[], sort_by=None, nested={}, search=None,
             within=None, has_key=None, **kwargs):
        filters = cls._generate_filters(model=model, nested=nested, search=search, within=within, has_key=has_key,
                                        **kwargs)
        query = cls._query_builder(model=model, filters=filters, include=include, expand=expand, sort_by=sort_by)

        if page is not None and per_page is not None:
            paginate = query.paginate(page, per_page, False)
            items = paginate.items
            total = paginate.total
        else:
            items = query.all()
            total = len(items)

        Find = collections.namedtuple('Find', ['items', 'total'])
        return Find(items=items, total=total)

    @classmethod
    def destroy(cls, instance):
        db.session.delete(instance)
        db.session.commit()
        return True
