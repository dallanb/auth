from ... import ma
from ..User import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    uuid = ma.auto_field()
    email = ma.auto_field()
    username = ma.auto_field()
    role_uuid = ma.auto_field()
    status_uuid = ma.auto_field()
