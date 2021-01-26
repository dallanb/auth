from marshmallow import fields, Schema
from marshmallow.validate import Length


class ResetPasswordSchema(Schema):
    token = fields.Str(required=True, validate=Length(equal=64))
    password = fields.Str(required=True)


reset_password_schema = ResetPasswordSchema()
