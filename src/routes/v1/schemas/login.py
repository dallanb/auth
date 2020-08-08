from marshmallow import fields, Schema


class LoginFormSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


login_form_schema = LoginFormSchema()
