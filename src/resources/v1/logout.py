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
        try:
            auth = request.headers.get('Authorization')
            if not auth:
                raise Exception('Missing authorization')
            auth_token = auth.split(" ")[1]
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.BAD_REQUEST)

        try:
            UserTokenModel.destroy_auth_token(auth_token=auth_token)
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.BAD_REQUEST)

        return DataResponse(data=False)
