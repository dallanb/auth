from flask import g
from flask_restful import marshal_with
from .schemas import dump_user_schema
from ...common.response import DataResponse
from ...common.auth import check_auth
from ...services import User, Token

from . import Base


class Status(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.token = Token()

    @marshal_with(DataResponse.marshallable())
    @check_auth
    def get(self):
        tokens = self.token.find(token=g.token)
        if not tokens.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        users = self.user.find(uuid=tokens.items[0].user_uuid)
        if not users.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        try:
            _ = self.token.decode_token(token=tokens.items[0].token)
        except ValueError as e:
            if 'destroy_token' in e.args:
                attr = self.token.generate_deactivate_token_attributes(username=users.items[0].username,
                                                                       kong_jwt_id=tokens.items[
                                                                           0].kong_jwt_id)
                token = self.token.assign_attr(instance=tokens.items[0], attr=attr)
                _ = self.token.save(instance=token)
            self.throw_error(http_code=self.code.UNAUTHORIZED)
        return DataResponse(
            data={
                'user': self.dump(
                    schema=dump_user_schema,
                    instance=users.items[0]
                )
            }
        )
