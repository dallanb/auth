from flask import request
from flask_restful import marshal_with
from ...common import DataResponse
from ...models import User, UserSchema

from . import Base


class Status(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def get(self):
        auth = request.headers.get('Authorization')
        if not auth:
            self.logger.error('Missing authorization')
            self.throw_error(self.code.BAD_REQUEST)

        auth_token = auth.split(" ")[1]

        user_id = User.decode_auth_token(auth_token)

        if isinstance(user_id, str):
            self.logger.info(user_id)
            self.throw_error(self.code.BAD_REQUEST)

        user = User.query.filter(User.id == user_id).first()

        user_result = UserSchema().dump(user)

        return DataResponse(data={'user': user_result})
