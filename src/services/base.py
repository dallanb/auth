import logging
from http import HTTPStatus
from sqlalchemy.exc import DataError, IntegrityError, StatementError

from ..common import Cache, DB, Event
from ..common.error import ManualException


class Base:
    def __init__(self):
        self.db = DB()
        self.cache = Cache()
        self.event = Event()
        self.logger = logging.getLogger(__name__)

    # @cache.memoize(timeout=1000)
    def _count(self, model):
        return self.db.count(model=model)

    def _find(self, model, **kwargs):
        try:
            return self.db.find(model=model, **kwargs)
        except AttributeError:
            self.logger.error(f'find error - AttributeError')
            self.error(code=HTTPStatus.BAD_REQUEST)
        except StatementError:
            self.logger.error(f'find error - StatementError')
            self.error(code=HTTPStatus.BAD_REQUEST)

    def _init(self, model, **kwargs):
        try:
            return self.db.init(model=model, **kwargs)
        except TypeError:
            self.logger.error(f'init error - TypeError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        except KeyError:
            self.logger.error(f'init error - KeyError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        except AttributeError:
            self.logger.error('init error - AttributeError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)

    def _add(self, instance):
        try:
            return self.db.add(instance=instance)
        except TypeError:
            self.logger.error(f'add error - TypeError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        except KeyError:
            self.logger.error(f'add error - KeyError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)

    def _commit(self):
        try:
            return self.db.commit()
        except DataError:
            self.logger.error(f'commit error - DataError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        except IntegrityError:
            self.logger.error(f'commit error - IntegrityError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        except StatementError:
            self.logger.error(f'commit error - StatementError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)

    def _save(self, instance):
        try:
            return self.db.save(instance=instance)
        except DataError:
            self.logger.error(f'save error - DataError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        except IntegrityError:
            self.logger.error(f'save error - IntegrityError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        except StatementError:
            self.logger.error(f'save error - StatementError')
            self.db.rollback()
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)

    def _destroy(self, instance):
        return self.db.destroy(instance=instance)

    def _rollback(self):
        return self.db.rollback()

    def _assign_attr(self, instance, attr):
        try:
            for k, v in attr.items():
                if not (hasattr(instance, k)):
                    raise KeyError(f'invalid key {k}')
                instance.__setattr__(k, v)
            return instance
        except ValueError as ex:
            self.logger.error(f'assign_attr error - ValueError')
            self.logger.error(ex)
            self.db.rollback()
            self.error(code=HTTPStatus.BAD_REQUEST)
        except KeyError as ex:
            self.logger.error(f'assign_attr error - KeyError')
            self.logger.error(ex)
            self.db.rollback()
            self.error(code=HTTPStatus.BAD_REQUEST)
        except AttributeError as ex:
            self.logger.error(f'assign_attr error - AttributeError')
            self.logger.error(ex)
            self.db.rollback()
            self.error(code=HTTPStatus.BAD_REQUEST)

    @staticmethod
    def dump(schema, instance, params=None):
        if params:
            for k, v in params.items():
                schema.context[k] = v
        return schema.dump(instance)

    @staticmethod
    def clean(schema, instance, **kwargs):
        return schema.load(instance, **kwargs)

    def notify(self, topic, value, key):
        self.event.send(topic=topic, value=value, key=key)

    @staticmethod
    def error(code, **kwargs):
        if code is None:
            raise ManualException()
        error_code = code.value
        msg = kwargs.get('msg', code.phrase)
        err = kwargs.get('err', None)
        raise ManualException(code=error_code, msg=msg, err=err)
