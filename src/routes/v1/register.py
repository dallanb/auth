from flask import request
from flask_restful import marshal_with

from . import Base
from .schemas import register_form_schema, dump_user_schema
from ...common.response import DataResponse
from ...services import User, InviteToken


class Register(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.invite_token = InviteToken()

    @marshal_with(DataResponse.marshallable())
    def post(self):
        data = self.clean(schema=register_form_schema, instance=request.get_json())

        # check the invite table if this token exists to avoid this user having to confirm their email again
        status = 'active' if data['token'] and self.invite_token.confirm_token(token=data['token'],
                                                                               email=data['email']) else 'pending'

        user = self.user.create(username=data['username'], email=data['email'], password=data['password'],
                                display_name=data['display_name'], country=data['country'], role='member',
                                status=status)
        return DataResponse(
            data={
                'user': self.dump(
                    schema=dump_user_schema,
                    instance=user
                )
            }
        )
