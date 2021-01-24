from marshmallow import fields, Schema
from marshmallow.validate import Length


class InviteSchema(Schema):
    token = fields.Str(required=True, validate=Length(equal=64))


invite_schema = InviteSchema()
