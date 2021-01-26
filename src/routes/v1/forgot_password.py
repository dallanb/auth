from flask import request
from flask_restful import marshal_with

from . import Base
from .schemas import forgot_password_schema
from ...common import TokenStatusEnum
from ...common.response import MessageResponse
from ...services import User, ResetPasswordToken


class ForgotPassword(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.reset_password_token = ResetPasswordToken()

    @marshal_with(MessageResponse.marshallable())
    def post(self):
        data = self.clean(schema=forgot_password_schema, instance=request.get_json())
        users = self.user.find(email=data['email'])
        if not users.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        if not users.items[0].status == TokenStatusEnum['active']:
            self.throw_error(http_code=self.code.BAD_REQUEST)
        self.reset_password_token.deactivate_tokens(email=data['email'])
        _ = self.reset_password_token.create(**data, status='active')
        return MessageResponse(message=self.code.OK.phrase)
