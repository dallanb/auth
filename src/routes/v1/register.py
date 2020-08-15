from flask import request
from flask_restful import marshal_with
from .schemas import register_form_schema, dump_user_schema, dump_token_schema
from ...common.response import DataResponse
from ...services import User, Token

from . import Base


class Register(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.token = Token()

    @marshal_with(DataResponse.marshallable())
    def post(self):
        data = self.clean(schema=register_form_schema, instance=request.get_json())
        user = self.user.create(username=data['username'], email=data['email'], password=data['password'],
                                role='member',
                                status='active')
        # _ = self.user.send_register_mail(user=user_result)
        attr = self.token.generate_token_attributes(uuid=user.uuid, username=user.username)
        token = self.token.create(**attr)
        return DataResponse(
            data={
                'user': self.dump(
                    schema=dump_user_schema,
                    instance=user
                ),
                'token': self.dump(
                    schema=dump_token_schema,
                    instance=token
                )['token']
            }
        )
