from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from ..schemas import LoginFormSchema
from ...models import UserModel, UserSchema, UserTokenModel, UserTokenSchema
from ...common import DataResponse, get_json
from . import Base


class Login(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def post(self):
        if not len(request.form) or not request.form.get('data', None):
            self.logger.error('Missing form data')
            self.throw_error(self.code.BAD_REQUEST)

        try:
            data = LoginFormSchema().load(get_json(request.form['data']))
        except ValidationError as err:
            self.logger.error(err.messages)
            self.throw_error(self.code.BAD_REQUEST)

        user = UserModel.query.filter(UserModel.email == data['email']).first()

        if not user:
            self.logger.error('User with provided credentials not found')
            self.throw_error(self.code.BAD_REQUEST)

        if not user.check_password(data['password']):
            self.logger.error('User with provided credentials not found')
            self.throw_error(self.code.BAD_REQUEST)

        user_result = UserSchema().dump(user)

        user_token = UserTokenModel.create_auth_token(uuid=user_result['uuid'], username=user_result['username'])

        if not user_token:
            self.logger.error('Issues authorizing auth token')
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)

        user_token_result = UserTokenSchema().dump(user_token)

        return DataResponse(data={'user': user_result, 'auth_token': user_token_result['token']})
