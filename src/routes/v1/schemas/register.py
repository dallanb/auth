from marshmallow import fields, Schema


class RegisterFormSchema(Schema):
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    display_name = fields.Str(required=True)
    country = fields.Str(required=True)
    token = fields.Str(required=False, missing=None)


register_form_schema = RegisterFormSchema()
