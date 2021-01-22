from flask_restful import marshal_with

from . import Base
from .schemas import invite_schema, dump_invite_token_schema
from ...common.response import DataResponse
from ...services import User, InviteToken


class Invite(Base):
    def __init__(self):
        Base.__init__(self)
        self.user = User()
        self.invite_token = InviteToken()

    @marshal_with(DataResponse.marshallable())
    def get(self, token):
        data = self.invite_token.clean(schema=invite_schema, instance={'token': token})
        invite_tokens = self.invite_token.find(**data, status='active')
        if not invite_tokens.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        # if invite_tokens.items[0].status == TokenStatusEnum['inactive']:
        #     self.throw_error(http_code=self.code.UNAUTHORIZED)
        return DataResponse(
            data={
                'invites': self.dump(
                    schema=dump_invite_token_schema,
                    instance=invite_tokens.items[0]
                )
            }
        )
