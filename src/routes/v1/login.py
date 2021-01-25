from flask import request
from flask_restful import marshal_with

from . import Base
from .schemas import login_form_schema, dump_user_schema, dump_access_token_schema
from ...common import generate_expiry, UserStatusEnum
from ...common.response import DataResponse
from ...models import User, AccessToken
from ...services import User, AccessToken, RefreshToken


class Login(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.access_token = AccessToken()
        self.refresh_token = RefreshToken()

    @marshal_with(DataResponse.marshallable())
    def post(self):
        data = self.clean(schema=login_form_schema, instance=request.get_json())
        users = self.user.find(email=data['email'])
        if not users.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        if data['password'] != users.items[0].password:
            self.throw_error(http_code=self.code.BAD_REQUEST, msg='User with provided credentials not found')
        if not users.items[0].status == UserStatusEnum['active']:
            self.throw_error(http_code=self.code.UNAUTHORIZED, msg=f'User account is {users.items[0].status.name}')

        refresh_expiry = generate_expiry(self.config['REFRESH_EXP'])
        attr = self.refresh_token.generate_token_attributes(uuid=users.items[0].uuid, username=users.items[0].username,
                                                            expiry=refresh_expiry)
        refresh_token = self.refresh_token.create(**attr)

        access_expiry = generate_expiry(self.config['ACCESS_EXP'])
        attr = self.access_token.generate_token_attributes(uuid=users.items[0].uuid, username=users.items[0].username,
                                                           expiry=access_expiry)
        access_token = self.access_token.create(**attr, refresh_token=refresh_token)

        # this looks disgusting please clean it up
        return DataResponse(
            data={
                'user': self.dump(
                    schema=dump_user_schema,
                    instance=users.items[0]
                ),
                'access_token': self.dump(
                    schema=dump_access_token_schema,
                    instance=access_token
                )['token'],
                'expiry': self.config['ACCESS_EXP']
            }
        ), 200, [('Set-Cookie', f'refresh_token={refresh_token.token}')]
