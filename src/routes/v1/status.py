from flask import g
from flask_restful import marshal_with
from .schemas import dump_user_schema
from ...common.response import DataResponse
from ...common.auth import check_auth
from ...models import User, Token
from ... import services

from . import Base


class Status(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    @check_auth
    def get(self):
        tokens = self.find(model=Token, token=g.token, status='active', not_found=self.code.NOT_FOUND)
        users = self.find(model=User, uuid=tokens.items[0].user_uuid, not_found=self.code.INTERNAL_SERVER_ERROR)
        try:
            _ = services.decode_token(token=tokens.items[0].token)
        except ValueError as e:
            if 'destroy_token' in e.args:
                attr = services.generate_deactivate_token_attributes(username=users.items[0].username,
                                                                     kong_jwt_id=tokens.items[
                                                                         0].kong_jwt_id)
                token = self.assign_attr(instance=tokens.items[0], attr=attr)
                _ = self.save(instance=token)
            self.throw_error(http_code=self.code.UNAUTHORIZED)
        return DataResponse(
            data={
                'user': self.dump(
                    schema=dump_user_schema,
                    instance=users.items[0]
                )
            }
        )
