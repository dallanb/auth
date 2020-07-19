import uuid
from flask import request
from flask_restful import marshal_with
from ...common import DataResponse
from ...models import UserTokenModel

from . import Base


class Logout(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def post(self):
        auth = request.headers.get('Authorization')
        if not auth:
            self.logger.error('Missing authorization')
            self.throw_error(self.code.BAD_REQUEST)

        auth_token = auth.split(" ")[1]

        UserTokenModel.destroy_auth_token(auth_token=auth_token)

        return DataResponse(data=False)
