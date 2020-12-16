from marshmallow import fields, Schema


class RegisterFormSchema(Schema):
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)


register_form_schema = RegisterFormSchema()
