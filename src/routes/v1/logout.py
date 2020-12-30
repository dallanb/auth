from flask import g
from flask_restful import marshal_with

from . import Base
from ...common import TokenStatusEnum
from ...common.auth import check_auth
from ...common.response import DataResponse
from ...services import User, AccessToken, RefreshToken


class Logout(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.access_token = AccessToken()
        self.refresh_token = RefreshToken()

    @marshal_with(DataResponse.marshallable())
    @check_auth
    def post(self):
        access_tokens = self.access_token.find(token=g.access_token, status=TokenStatusEnum['active'])
        if not access_tokens.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        users = self.user.find(uuid=access_tokens.items[0].user_uuid)
        if not users.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        attr = self.access_token.generate_deactivate_token_attributes(username=users.items[0].username,
                                                                      kong_jwt_id=access_tokens.items[0].kong_jwt_id)
        access_token = self.access_token.assign_attr(instance=access_tokens.items[0], attr=attr)
        _ = self.access_token.save(instance=access_token)

        _ = self.refresh_token.update(uuid=access_tokens.items[0].refresh_token_uuid, status='inactive')

        return DataResponse(data=False)
