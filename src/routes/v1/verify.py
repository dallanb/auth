from flask import request
from flask_restful import marshal_with

from . import Base
from .schemas import verify_schema
from ...common import TokenStatusEnum
from ...common.response import MessageResponse
from ...services import User, VerifyToken


class Verify(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.verify_token = VerifyToken()

    @marshal_with(MessageResponse.marshallable())
    def post(self):
        data = self.verify_token.clean(schema=verify_schema, instance=request.get_json())
        verify_tokens = self.verify_token.find(**data)
        if not verify_tokens.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        if not verify_tokens.items[0].status == TokenStatusEnum['active']:
            self.throw_error(http_code=self.code.UNAUTHORIZED, msg='Token no longer valid')
        users = self.user.find(email=verify_tokens.items[0].email)
        if not users.total:
            self.throw_error(http_code=self.code.INTERNAL_SERVER_ERROR)
        self.user.apply(instance=users.items[0], status='active')
        return MessageResponse(message=self.code.OK.phrase)
