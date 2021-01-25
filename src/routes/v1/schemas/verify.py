from marshmallow import fields, Schema
from marshmallow.validate import Length


class VerifySchema(Schema):
    token = fields.Str(required=True, validate=Length(equal=64))


verify_schema = VerifySchema()
