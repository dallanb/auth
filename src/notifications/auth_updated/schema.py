from marshmallow import Schema
from webargs import fields


class AuthUpdatedSchema(Schema):
    uuid = fields.UUID(attribute='user.uuid')
    username = fields.String(attribute='user.username')
    email = fields.String(attribute='user.email')
    status = fields.String(attribute='user.status.name')
