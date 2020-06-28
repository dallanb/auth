from marshmallow_enum import EnumField
from ... import ma
from ..Role import Role
from ...common import RoleEnum


class RoleSchema(ma.SQLAlchemySchema):
    name = EnumField(RoleEnum)

    class Meta:
        model = Role
        load_instance = True

    uuid = ma.auto_field()
