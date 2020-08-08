from flask import request
from flask_restful import marshal_with
from .schemas import login_form_schema, dump_user_schema, dump_token_schema
from ...models import User, Token
from ...common.response import DataResponse
from ... import services

from . import Base


class Login(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def post(self):
        data = self.clean(schema=login_form_schema, instance=request.get_json())
        users = self.find(model=User, email=data['email'], not_found=self.code.NOT_FOUND)
        if data['password'] != users.items[0].password:
            self.throw_error(http_code=self.code.BAD_REQUEST, msg='User with provided credentials not found')
        user_result = self.dump(schema=dump_user_schema, instance=users.items[0])
        token = self.init(model=Token)
        attr = services.generate_token_attributes(uuid=user_result['uuid'], username=user_result['username'])
        token = self.assign_attr(instance=token, attr=attr)
        token = self.save(instance=token)
        token_result = self.dump(schema=dump_token_schema, instance=token)
        return DataResponse(
            data={
                'user': user_result,
                'token': token_result['token']
            }
        )
