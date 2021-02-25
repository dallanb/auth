from marshmallow import Schema
from webargs import fields


class VerifyCreatedSchema(Schema):
    uuid = fields.UUID(attribute='verify.uuid')
    token = fields.String(attribute='verify.token')
    email = fields.String(attribute='verify.email')
