from flask import request
from flask_restful import marshal_with
from marshmallow import ValidationError
from ..schemas import RegisterFormSchema
from ...models import UserModel, UserSchema, UserTokenModel, UserTokenSchema
from ...common import DataResponse, get_json, UserRoleEnum, UserStatusEnum

from . import Base


class Register(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def post(self):
        if not len(request.form) or not request.form.get('data', None):
            self.logger.error('Missing form data')
            self.throw_error(self.code.BAD_REQUEST)

        try:
            data = RegisterFormSchema().load(get_json(request.form['data']))
        except ValidationError as err:
            self.logger.error(err.messages)
            self.throw_error(self.code.BAD_REQUEST)

        role = UserModel.find_role(UserRoleEnum.member)
        status = UserModel.find_status(UserStatusEnum.active)

        user = UserModel(username=data['username'], email=data['email'], password=data['password'], role=role,
                         status=status)

        self.db.session.add(user)
        self.db.session.commit()

        user_result = UserSchema().dump(user)

        user_token = UserTokenModel.create_auth_token(uuid=user_result['uuid'], username=user_result['username'])

        if not user_token:
            self.logger.error('Issues authorizing auth token')
            self.throw_error(self.code.INTERNAL_SERVER_ERROR)

        user_token_result = UserTokenSchema().dump(user_token)

        return DataResponse(data={'user': user_result, 'auth_token': user_token_result['token']})
