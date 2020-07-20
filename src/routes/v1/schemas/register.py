from marshmallow import fields, Schema


class RegisterFormSchema(Schema):
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
