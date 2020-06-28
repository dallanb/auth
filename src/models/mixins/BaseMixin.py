from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.event import listen
from ... import db
from ..utils import generate_uuid, time_now


class BaseMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(UUIDType(binary=False), unique=True, nullable=False)
    ctime = db.Column(db.BigInteger)
    mtime = db.Column(db.BigInteger)

    @staticmethod
    def before_insert(mapper, connection, target):
        target.ctime = time_now()
        target.uuid = generate_uuid()
        return

    @staticmethod
    def before_update(mapper, connection, target):
        target.mtime = time_now()
        return

    @classmethod
    def register(cls):
        listen(cls, 'before_insert', cls.before_insert)
        listen(cls, 'before_update', cls.before_update)
