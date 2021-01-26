from marshmallow import Schema
from marshmallow_enum import EnumField
from webargs import fields

from ....common.enums import TokenStatusEnum


class DumpForgotPasswordTokenSchema(Schema):
    uuid = fields.UUID()
    token = fields.String()
    email = fields.String()
    status = EnumField(TokenStatusEnum)


dump_forgot_password_token_schema = DumpForgotPasswordTokenSchema()
