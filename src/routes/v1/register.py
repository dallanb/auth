from flask import request
from flask_restful import marshal_with
from .schemas import register_form_schema, dump_user_schema, dump_token_schema
from ...models import User, Token
from ...common.response import DataResponse
from ... import services

from . import Base


class Register(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def post(self):
        data = self.clean(schema=register_form_schema, instance=request.get_json())
        user = self.init(model=User, username=data['username'], email=data['email'], password=data['password'],
                         role='member',
                         status='active')
        user = self.save(instance=user)
        user_result = self.dump(schema=dump_user_schema, instance=user)
        _ = services.send_register_mail(user=user_result)
        token = self.init(model=Token)
        attr = services.generate_token_attributes(uuid=user_result['uuid'], username=user_result['username'])
        token = self.assign_attr(instance=token, attr=attr)
        token = self.save(instance=token)
        token_result = self.dump(schema=dump_token_schema, instance=token)
        return DataResponse(data={'user': user_result, 'token': token_result['token']})
