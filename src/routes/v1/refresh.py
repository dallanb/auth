from flask import g, request
from flask_restful import marshal_with
from .schemas import dump_user_schema
from ...common.response import DataResponse
from ...common.auth import check_auth
from ...services import User, Token

from . import Base


class Refresh(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.token = Token()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        refresh_token = request.cookies.get('refresh_token')
        if not refresh_token:
            self.throw_error(http_code=self.code.BAD_REQUEST)

        return DataResponse(
            data={
                'user': self.dump(
                    schema=dump_user_schema,
                    instance=users.items[0]
                )
            }
        )
