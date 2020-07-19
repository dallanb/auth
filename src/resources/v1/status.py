import uuid
from flask import request
from flask_restful import marshal_with
from ...common import DataResponse
from ...models import UserModel, UserSchema, UserTokenModel
from ... import cache

from . import Base


class Status(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @cache.cached(timeout=60)
    def get(self):
        auth = request.headers.get('Authorization')
        if not auth:
            self.logger.error('Missing authorization')
            self.throw_error(self.code.BAD_REQUEST)

        auth_token = auth.split(" ")[1]

        is_active = UserTokenModel.is_active(token=auth_token)
        if not is_active:
            self.logger.info('Invalid token. Please log in again.')
            self.throw_error(self.code.UNAUTHORIZED)

        token = UserTokenModel.decode_token(token=auth_token)
        try:
            uuid.UUID(token['sub'])
        except ValueError:
            self.logger.info(token)
            self.throw_error(self.code.BAD_REQUEST)

        user = UserModel.query.filter(UserModel.uuid == token['sub']).first()

        user_result = UserSchema().dump(user)

        return DataResponse(data={'user': user_result})
