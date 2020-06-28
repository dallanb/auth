from sqlalchemy.event import listens_for
from sqlalchemy_utils import UUIDType
from marshmallow_enum import EnumField
from ..common import RoleEnum
from .. import db, ma
from .Base import Base
from .utils import generate_uuid


class Role(Base):
    __tablename__ = 'role'
    uuid = db.Column(UUIDType(binary=False), unique=True, nullable=False)
    name = db.Column(db.Enum(RoleEnum), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@listens_for(Role, 'before_insert')
def before_insert(mapper, connect, self):
    self.uuid = generate_uuid()


@listens_for(Role, 'before_update')
def before_update(mapper, connect, self):
    return


class RoleSchema(ma.SQLAlchemySchema):
    name = EnumField(RoleEnum)

    class Meta:
        model = Role
        load_instance = True

    uuid = ma.auto_field()
