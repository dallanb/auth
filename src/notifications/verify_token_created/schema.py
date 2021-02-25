from marshmallow import Schema
from webargs import fields


class VerifyTokenCreatedSchema(Schema):
    uuid = fields.UUID(attribute='verify_token.uuid')
    token = fields.String(attribute='verify_token.token')
    email = fields.String(attribute='verify_token.email')
