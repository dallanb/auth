from marshmallow_enum import EnumField
from ... import ma
from ..UserRole import UserRole
from ...common import UserRoleEnum


class UserRoleSchema(ma.SQLAlchemySchema):
    name = EnumField(UserRoleEnum)

    class Meta:
        model = UserRole
        load_instance = True

    uuid = ma.auto_field()
