import collections
import inflect
from sqlalchemy import inspect
from ..common.error import *
from ..common.cleaner import Cleaner
from .. import db


class DB:
    @classmethod
    # Helpers
    def _query_builder(cls, model, filters=[], expand=[], include=[], sort_by=None, limit=None, offset=None):
        query = db.session.query(model)
        for k, v in filters:
            if k == 'like':
                for like_k, like_v in v:
                    search = "%{}%".format(like_v)
                    query = query.filter(like_k.like(search))
            if k == 'equal':
                for equal_k, equal_v in v:
                    query = query.filter(equal_k == equal_v)
            if k == 'gt':
                for gt_k, gt_v in v:
                    query = query.filter(gt_k > gt_v)
            if k == 'gte':
                for gte_k, gte_v in v:
                    query = query.filter(gte_k >= gte_v)
            if k == 'lt':
                for lt_k, lt_v in v:
                    query = query.filter(lt_k < lt_v)
            if k == 'lte':
                for lte_k, lte_v in v:
                    query = query.filter(lte_k <= lte_v)
        for i, k in enumerate(expand):
            tables = k.split('.')
            for j, table in enumerate(tables):
                if j == 0:
                    # query = query.join(getattr(model, table))
                    options = db.lazyload(getattr(model, table))
                else:
                    nested_class = cls._get_class_by_tablename(tables[j - 1])
                    # query = query.join(getattr(nested_class, table))
                    options = options.lazyload(getattr(nested_class, table))
            if i == len(expand) - 1:
                query = query.options(options)
        for i, k in enumerate(include):
            tables = k.split('.')
            for j, table in enumerate(tables):
                if j == 0:
                    # query = query.join(getattr(model, table))
                    options = db.joinedload(getattr(model, table))
                else:
                    nested_class = cls._get_class_by_tablename(cls._singularize(tables[j - 1]))
                    # query = query.join(getattr(nested_class, table))
                    options = options.joinedload(getattr(nested_class, table))
            if i == len(include) - 1:
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
    # Methods
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
    def find(cls, model, page=None, per_page=None, expand=[], include=[], nested={}, **kwargs):
        filters = []
        for k, v in kwargs.items():
            filters.append(('equal', [(getattr(model, k), v)]))

        for k, v in nested.items():
            nested_class = cls._get_class_by_tablename(k)
            for nested_k, nested_v in v.items():
                filters.append(('equal', [(getattr(nested_class, nested_k), nested_v)]))

        query = cls._query_builder(model=model, filters=filters, include=include, expand=expand)

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
