from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields
from ....common.enums import TokenStatusEnum


class DumpTokenSchema(Schema):
    uuid = fields.UUID()
    token = fields.String()
    kong_jwt_id = fields.UUID()
    status = EnumField(TokenStatusEnum)


dump_token_schema = DumpTokenSchema()
