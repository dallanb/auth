from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.event import listen
from ... import db
from ...common.utils import camel_to_snake, generate_uuid, time_now


class BaseMixin(object):

    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    uuid = db.Column(UUIDType(binary=False), primary_key=True, unique=True, nullable=False)
    ctime = db.Column(db.BigInteger, default=time_now)
    mtime = db.Column(db.BigInteger, onupdate=time_now)

    @staticmethod
    def init(mapper, connection, target):
        target['uuid'] = generate_uuid()
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
