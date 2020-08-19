from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.event import listen
from ... import db
from ...common.utils import camel_to_snake, time_now


class StatusMixin(object):

    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    ctime = db.Column(db.BigInteger, default=time_now)
    mtime = db.Column(db.BigInteger, onupdate=time_now)

    @staticmethod
    def init(mapper, connection, target):
        return

    @staticmethod
    def before_insert(mapper, connection, target):
        return

    @staticmethod
    def before_update(mapper, connection, target):
        return

    @classmethod
    def register(cls):
        listen(cls, 'init', cls.init)
        listen(cls, 'before_insert', cls.before_insert)
        listen(cls, 'before_update', cls.before_update)
