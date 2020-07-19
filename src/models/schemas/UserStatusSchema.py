from marshmallow_enum import EnumField
from ... import ma
from ..UserStatus import UserStatus
from ...common import UserStatusEnum


class UserStatusSchema(ma.SQLAlchemySchema):
    name = EnumField(UserStatusEnum)

    class Meta:
        model = UserStatus
        load_instance = True

    uuid = ma.auto_field()
