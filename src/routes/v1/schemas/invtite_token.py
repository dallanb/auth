from marshmallow import Schema, post_dump
from marshmallow_enum import EnumField
from webargs import fields
from ....common.enums import TokenStatusEnum


class DumpInviteTokenSchema(Schema):
    uuid = fields.UUID()
    token = fields.String()
    email = fields.String()
    status = EnumField(TokenStatusEnum)


dump_invite_token_schema = DumpInviteTokenSchema()
