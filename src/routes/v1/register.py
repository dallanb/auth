from flask import request
from flask_restful import marshal_with

from . import Base
from .schemas import register_form_schema, dump_user_schema
from ...common.response import DataResponse
from ...services import User, AccessToken, RefreshToken


class Register(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.access_token = AccessToken()
        self.refresh_token = RefreshToken()

    @marshal_with(DataResponse.marshallable())
    def post(self):
        data = self.clean(schema=register_form_schema, instance=request.get_json())
        user = self.user.create(username=data['username'], email=data['email'], password=data['password'],
                                role='member',
                                status='active')
        return DataResponse(
            data={
                'user': self.dump(
                    schema=dump_user_schema,
                    instance=user
                )
            }
        )
