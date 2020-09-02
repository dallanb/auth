from flask import g
from flask_restful import marshal_with

from . import Base
from .schemas import dump_user_schema
from ...common.auth import check_auth
from ...common.response import DataResponse
from ...common.utils import decode_token
from ...services import User, AccessToken


class Status(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.access_token = AccessToken()

    @marshal_with(DataResponse.marshallable())
    @check_auth
    def get(self):
        access_tokens = self.access_token.find(token=g.access_token)
        if not access_tokens.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        users = self.user.find(uuid=access_tokens.items[0].user_uuid)
        if not users.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        try:
            _ = decode_token(token=access_tokens.items[0].token)
        except ValueError as e:
            if 'destroy_token' in e.args:
                attr = self.access_token.generate_deactivate_token_attributes(username=users.items[0].username,
                                                                              kong_jwt_id=access_tokens.items[
                                                                                  0].kong_jwt_id)
                access_token = self.access_token.assign_attr(instance=access_tokens.items[0], attr=attr)
                _ = self.access_token.save(instance=access_token)
            self.throw_error(http_code=self.code.UNAUTHORIZED)
        return DataResponse(
            data={
                'user': self.dump(
                    schema=dump_user_schema,
                    instance=users.items[0]
                )
            }
        )
