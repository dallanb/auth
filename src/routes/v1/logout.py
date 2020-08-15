from flask import request, g
from flask_restful import marshal_with
from ...common.response import DataResponse
from ...common.auth import check_auth
from ...services import User, Token

from . import Base


class Logout(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.token = Token()

    @marshal_with(DataResponse.marshallable())
    @check_auth
    def post(self):
        tokens = self.token.find(token=g.token)
        if not tokens.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        users = self.user.find(uuid=tokens.items[0].user_uuid)
        if not users.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        attr = self.token.generate_deactivate_token_attributes(username=users.items[0].username,
                                                               kong_jwt_id=tokens.items[0].kong_jwt_id)
        token = self.assign_attr(instance=tokens.items[0], attr=attr)
        _ = self.save(instance=token)
        return DataResponse(data=False)
