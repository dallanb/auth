from marshmallow import Schema
from webargs import fields


class AuthCreatedSchema(Schema):
    uuid = fields.UUID(attribute='user.uuid')
    username = fields.String(attribute='user.username')
    email = fields.String(attribute='user.email')
    display_name = fields.String()
    country = fields.String()
    status = fields.String(attribute='user.status.name')
