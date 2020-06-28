from flask import request
from flask_restful import marshal_with
from ...common import DataResponse
from ...models import User, BlacklistToken

from . import Base


class Logout(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(DataResponse.marshallable())
    def post(self):
        auth = request.headers.get('Authorization')
        if not auth:
            self.logger.error('Missing authorization')
            self.throw_error(self.code.BAD_REQUEST)

        auth_token = auth.split(" ")[1]

        user_id = User.decode_auth_token(auth_token)

        if isinstance(user_id, str):
            self.logger.info(user_id)
            self.throw_error(self.code.BAD_REQUEST)

        blacklist_token = BlacklistToken(token=auth_token)
        self.db.session.add(blacklist_token)
        self.db.session.commit()

        return DataResponse(data=False)
