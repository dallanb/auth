from flask import request
from flask_restful import marshal_with

from . import Base
from .schemas import dump_access_token_schema
from ...common.response import DataResponse
from ...common.utils import decode_token
from ...services import User, RefreshToken, AccessToken


class Refresh(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.access_token = AccessToken()
        self.refresh_token = RefreshToken()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        refresh_token = request.cookies.get('refresh_token')
        if not refresh_token:
            self.throw_error(http_code=self.code.BAD_REQUEST)

        # all of this needs to be cleaned up also status api
        self.logger.info(refresh_token)
        refresh_tokens = self.refresh_token.find(token=refresh_token)
        if not refresh_tokens.total:
            self.throw_error(http_code=self.code.BAD_REQUEST)
        try:
            _ = decode_token(token=refresh_token)
        except ValueError as e:
            if 'destroy_token' in e.args:
                _ = self.refresh_token.apply(instance=refresh_tokens.items[0], status='inactive')
            self.throw_error(http_code=self.code.UNAUTHORIZED)

        users = self.user.find(uuid=refresh_tokens.items[0].user_uuid)
        if not users.total:
            self.throw_error(http_code=self.code.INTERNAL_SERVER_ERROR)
        access_tokens = self.access_token.find(user_uuid=refresh_tokens.items[0].user_uuid, status='active')
        if access_tokens.total:
            for access_token in access_tokens.items:
                attr = self.access_token.generate_deactivate_token_attributes(username=users.items[0].username,
                                                                              kong_jwt_id=access_token.kong_jwt_id)
                _ = self.access_token.apply(instance=access_token, **attr)

        # create new access token
        attr = self.access_token.generate_token_attributes(uuid=users.items[0].uuid, username=users.items[0].username)
        access_token = self.access_token.create(**attr)

        return DataResponse(
            data={
                'access_token': self.dump(
                    schema=dump_access_token_schema,
                    instance=access_token
                )['token']
            }
        )