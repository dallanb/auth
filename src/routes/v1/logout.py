from flask import request, g
from flask_restful import marshal_with
from ...common.response import DataResponse
from ...common.auth import check_auth
from ...models import Token, User
from ... import services

from . import Base


class Logout(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_auth
    def post(self):
        tokens = self.find(model=Token, token=g.token, not_found=self.code.NOT_FOUND)
        users = self.find(model=User, uuid=tokens.items[0].user_uuid, not_found=self.code.NOT_FOUND)
        attr = services.generate_deactivate_token_attributes(username=users.items[0].username, kong_jwt_id=tokens.items[0].kong_jwt_id)
        token = self.assign_attr(instance=tokens.items[0], attr=attr)
        _ = self.save(instance=token)
        return DataResponse(data=False)
