from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields
from ....common.enums import UserStatusEnum, UserRoleEnum


class DumpUserSchema(Schema):
    uuid = fields.UUID()
    email = fields.Email()
    username = fields.String()
    role = EnumField(UserRoleEnum)
    status = EnumField(UserStatusEnum)


dump_user_schema = DumpUserSchema()
