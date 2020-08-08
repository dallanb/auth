from flask_restful import marshal_with
from ...common import MessageResponse

from . import Base


class Ping(Base):
    def __init__(self):
        Base.__init__(self)

    @marshal_with(MessageResponse.marshallable())
    def get(self):
        return MessageResponse(message='pong')
