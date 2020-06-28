from .utils import time_now
from .. import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    ctime = db.Column(db.BigInteger, default=time_now())
    mtime = db.Column(db.BigInteger, default=time_now(), onupdate=time_now())
