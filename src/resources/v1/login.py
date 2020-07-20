from flask import request
from flask_restful import marshal_with
from ..schemas import LoginFormSchema
from ...models import UserModel, UserSchema, UserTokenModel, UserTokenSchema
from ...common import DataResponse, get_json
from . import Base


class Login(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def post(self):
        # get request payload
        try:
            data = LoginFormSchema().load(get_json(request.form['data']))
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.BAD_REQUEST)

        # query auth_db for user in request payload
        try:
            user = UserModel.query.filter(UserModel.email == data['email']).first()
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.BAD_REQUEST)

        # check whether the password passed in is valid
        try:
            if not user.check_password(data['password']):
                raise Exception('User with provided credentials not found')
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.BAD_REQUEST)

        # dump user result instance
        try:
            user_result = UserSchema().dump(user)
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)

        # create an auth in auth_db and also kong jwt db
        try:
            user_token = UserTokenModel.create_auth_token(uuid=user_result['uuid'], username=user_result['username'])
            if not user_token:
                raise Exception('Issues authorizing auth token')
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)

        # dump user token model instance
        try:
            user_token_result = UserTokenSchema().dump(user_token)
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)

        return DataResponse(data={'user': user_result, 'auth_token': user_token_result['token']})
