from flask import request
from flask_restful import marshal_with
from ..schemas import RegisterFormSchema
from ...models import UserModel, UserSchema, UserTokenModel, UserTokenSchema
from ...common import DataResponse, get_json, UserRoleEnum, UserStatusEnum

from . import Base


class Register(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def post(self):
        # get request payload
        try:
            data = RegisterFormSchema().load(get_json(request.form['data']))
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.BAD_REQUEST)

        # query auth_db for member role row
        try:
            role = UserModel.find_role(UserRoleEnum.member)
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)

        # query auth_db for active status row
        try:
            status = UserModel.find_status(UserStatusEnum.active)
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)

        # create user in auth_db
        try:
            user = UserModel(username=data['username'], email=data['email'], password=data['password'], role=role,
                             status=status)
            self.db.session.add(user)
            self.db.session.commit()
        except Exception as e:
            self.logger.error(e)
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)

        # dump user model instance
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
