from marshmallow import fields, Schema


class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)


forgot_password_schema = ForgotPasswordSchema()
