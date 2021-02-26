from marshmallow import Schema
from webargs import fields


class InviteTokenCreatedSchema(Schema):
    uuid = fields.UUID(attribute='invite_token.uuid')
    token = fields.String(attribute='invite_token.token')
    email = fields.String(attribute='invite_token.email')
