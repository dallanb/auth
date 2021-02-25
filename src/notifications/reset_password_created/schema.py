from marshmallow import Schema
from webargs import fields


class ResetPasswordCreatedSchema(Schema):
    uuid = fields.UUID(attribute='reset_password.uuid')
    token = fields.String(attribute='reset_password.token')
    email = fields.String(attribute='reset_password.email')
