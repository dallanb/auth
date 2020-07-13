import uuid
from flask import request
from flask_restful import marshal_with
from ...common import DataResponse
from ...models import UserModel, UserSchema

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

        user_uuid = UserModel.decode_auth_token(auth_token)

        try:
            user_uuid = uuid.UUID(user_uuid)
        except ValueError:
            self.logger.info(user_uuid)
            self.throw_error(self.code.BAD_REQUEST)


        user = UserModel.query.filter(UserModel.uuid == user_uuid).first()

        user_result = UserSchema().dump(user)

        return DataResponse(data={'user': user_result})
