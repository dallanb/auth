from flask import request
from flask_restful import marshal_with

from . import Base
from .schemas import reset_password_schema
from ...common import TokenStatusEnum, UserStatusEnum
from ...common.response import MessageResponse
from ...services import User, ResetPasswordToken


class ResetPassword(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.reset_password_token = ResetPasswordToken()

    @marshal_with(MessageResponse.marshallable())
    def post(self):
        data = self.clean(schema=reset_password_schema, instance=request.get_json())
        reset_password_tokens = self.reset_password_token.find(token=data['token'])
        if not reset_password_tokens.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        if not reset_password_tokens.items[0].status == TokenStatusEnum['active']:
            self.throw_error(http_code=self.code.UNAUTHORIZED, msg='Token no longer valid')
        reset_password_token = reset_password_tokens.items[0]
        self.reset_password_token.deactivate_tokens(email=reset_password_token.email)
        users = self.user.find(email=reset_password_token.email)
        if not users.total:
            self.throw_error(http_code=self.code.INTERNAL_SERVER_ERROR)
        if not users.items[0].status == UserStatusEnum['active']:
            self.throw_error(http_code=self.code.UNAUTHORIZED, msg='User is not valid')
        self.user.apply(instance=users.items[0], password=data['password'])
        return MessageResponse(message=self.code.OK.phrase)
