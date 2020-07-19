from marshmallow_enum import EnumField
from ... import ma
from ..UserToken import UserToken
from ...common import UserTokenStatusEnum


class UserTokenSchema(ma.SQLAlchemySchema):
    status = EnumField(UserTokenStatusEnum)

    class Meta:
        model = UserToken
        load_instance = True

    uuid = ma.auto_field()
    token = ma.auto_field()
    kong_jwt_id = ma.auto_field()
