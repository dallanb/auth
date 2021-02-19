import collections
import re

import inflect
from sqlalchemy import inspect, or_, and_

from .. import db
from ..common.cleaner import Cleaner
from ..common.error import *


class DB:
    # Helpers

    @staticmethod
    def _query_builder(model, filters, expand=None, include=None, sort_by=None, limit=None,
                       offset=None):
        query = db.session.query(model)
        for logic_operator, filter_arr in filters:
            criterion = []
            for key, value in filter_arr:
                if key == 'like':
                    for like_k, like_v in value:
                        like_format = "%{}%".format(like_v)
                        criterion.append(like_k.like(like_format))
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
            options = db.joinedload(getattr(model, k))
            query = query.options(options)
        for i, k in enumerate(include):
            options = db.joinedload(getattr(model, k))
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

    @staticmethod
    def _get_class_by_tablename(tablename):
        for c in db.Model._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
                return c

    @staticmethod
    def _is_pending(instance):
        inspection = inspect(instance)
        return inspection.pending

    @staticmethod
    def _get_cache_key(model, query):
        return f"{model.__tablename__}:{str(query)}"

    @staticmethod
    def _pluralize(tablename):
        p = inflect.engine()
        return p.plural_noun(tablename)

    @staticmethod
    def _singularize(tablename):
        p = inflect.engine()
        return p.singular_noun(tablename)

    @staticmethod
    def _generate_equal_filter(model, **kwargs):
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

    def _generate_nested_filter(self, nested):
        nested_filter = []
        for k, v in nested.items():
            nested_class = self._get_class_by_tablename(k)
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

    @staticmethod
    def _generate_in_filter(model, within):
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

    @staticmethod
    def _generate_has_key_filter(model, has_key):
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

    def _generate_filters(self, model, nested=None, within=None, has_key=None, **kwargs):
        filters = []

        if len(kwargs):
            filters.extend(self._generate_equal_filter(model=model, **kwargs))

        if nested:
            filters.extend(self._generate_nested_filter(nested=nested))

        if within:
            filters.extend(self._generate_in_filter(model=model, within=within))

        if has_key:
            filters.extend(self._generate_has_key_filter(model=model, has_key=has_key))

        return filters

    def clean_query(self, model, expand=None, include=None, sort_by=None, nested=None,
                    within=None, has_key=None, **kwargs):
        if include is None:
            include = []

        if expand is None:
            expand = []

        filters = self._generate_filters(model=model, nested=nested, within=within, has_key=has_key,
                                         **kwargs)
        query = self._query_builder(model=model, filters=filters, include=include, expand=expand,
                                    sort_by=sort_by)
        return query

    @staticmethod
    def run_query(query, **kwargs):
        page = kwargs.get('page', None)
        per_page = kwargs.get('per_page', None)

        if page is not None and per_page is not None:
            paginate = query.paginate(page, per_page, False)
            items = paginate.items
            total = paginate.total
        else:
            items = query.all()
            total = len(items)

        Find = collections.namedtuple('Find', ['items', 'total'])
        return Find(items=items, total=total)

    # Methods

    @staticmethod
    def init(model, **kwargs):
        return model(**kwargs)

    @staticmethod
    def count(model):
        return db.session.query(model).count()

    # add an instance without saving it to the db

    def add(self, instance):
        if not instance:
            raise MissingParamError(instance.__tablename__)
        if not Cleaner().is_mapped(instance):
            raise InvalidTypeError(instance.__tablename__, 'mapped')

        if not self._is_pending(instance):
            db.session.add(instance)
        return instance

    @staticmethod
    def commit():
        db.session.commit()

    def save(self, instance):
        self.add(instance=instance)
        self.commit()
        return instance

    # TODO: Consider using dataclass instead of a named tuple
    def find(self, model, page=None, per_page=None, **kwargs):
        query = self.clean_query(model=model, **kwargs)
        return self.run_query(query=query, page=page, per_page=per_page)

    @staticmethod
    def delete(instance):
        db.session.delete(instance)
        return True

    def destroy(self, instance):
        self.delete(instance=instance)
        db.session.commit()
        return True

    @staticmethod
    def rollback():
        db.session.rollback()
