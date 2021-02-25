from marshmallow import Schema
from webargs import fields


class ResetPasswordCreatedSchema(Schema):
    uuid = fields.UUID(attribute='reset_password_token.uuid')
    token = fields.String(attribute='reset_password_token.token')
    email = fields.String(attribute='reset_password_token.email')
