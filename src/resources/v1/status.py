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
        try:
            auth = request.headers.get('Authorization')
            if not auth:
                raise Exception('Missing authorization')
            auth_token = auth.split(" ")[1]
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.BAD_REQUEST)

        try:
            is_active = UserTokenModel.is_active(token=auth_token)
            if not is_active:
                raise Exception('Invalid token. Please log in again.')
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.UNAUTHORIZED)

        try:
            token = UserTokenModel.decode_token(token=auth_token)
        except ValueError as e:
            if 'destroy_token' in e.args:
                UserTokenModel.destroy_auth_token(auth_token=auth_token)  # destroy the token
            self.logger.error(e)
            self.throw_error(self.code.UNAUTHORIZED)

        # query auth_db for user in request payload
        try:
            user = UserModel.query.filter(UserModel.uuid == token['sub']).first()
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)

        # dump user model instance
        try:
            user_result = UserSchema().dump(user)
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)

        return DataResponse(data={'user': user_result})
