from sqlalchemy.event import listens_for
from sqlalchemy_utils import UUIDType
from marshmallow_enum import EnumField
from ..common import StatusEnum
from .. import db, ma
from .Base import Base
from .utils import generate_uuid


class Status(Base):
    __tablename__ = 'status'
    uuid = db.Column(UUIDType(binary=False), unique=True, nullable=False)
    name = db.Column(db.Enum(StatusEnum), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@listens_for(Status, 'before_insert')
def before_insert(mapper, connect, self):
    self.uuid = generate_uuid()


@listens_for(Status, 'before_update')
def before_update(mapper, connect, self):
    return


class StatusSchema(ma.SQLAlchemySchema):
    name = EnumField(StatusEnum)

    class Meta:
        model = Status
        load_instance = True

    uuid = ma.auto_field()
