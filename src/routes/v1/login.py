from flask import request
from flask_restful import marshal_with
from .schemas import login_form_schema, dump_user_schema, dump_token_schema
from ...models import User, Token
from ...common.response import DataResponse
from ...services import User, Token

from . import Base


class Login(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.token = Token()

    @marshal_with(DataResponse.marshallable())
    def post(self):
        data = self.clean(schema=login_form_schema, instance=request.get_json())
        users = self.user.find(email=data['email'])
        if not users.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        if data['password'] != users.items[0].password:
            self.throw_error(http_code=self.code.BAD_REQUEST, msg='User with provided credentials not found')

        attr = self.token.generate_token_attributes(uuid=users.items[0].uuid, username=users.items[0].username)
        token = self.token.create(**attr)
        return DataResponse(
            data={
                'user': self.dump(
                    schema=dump_user_schema,
                    instance=users.items[0]
                ),
                'token': self.dump(
                    schema=dump_token_schema,
                    instance=token
                )['token']
            }
        )
