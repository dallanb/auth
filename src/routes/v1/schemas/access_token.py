from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields
from ....common.enums import TokenStatusEnum


class DumpAccessTokenSchema(Schema):
    uuid = fields.UUID()
    token = fields.String()
    kong_jwt_id = fields.UUID()
    status = EnumField(TokenStatusEnum)


dump_access_token_schema = DumpAccessTokenSchema()
