import logging

from .base import Base
from ..common.mail import Mail
from ..common.utils import generate_uuid, encode_token
from ..models import RefreshToken as RefreshTokenModel


class RefreshToken(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.refresh_token_model = RefreshTokenModel
        self.mail = Mail()

    def find(self, **kwargs):
        return Base.find(self, model=self.refresh_token_model, **kwargs)

    def create(self, **kwargs):
        access_token = self.init(model=self.refresh_token_model, **kwargs)
        return self.save(instance=access_token)

    def generate_token_attributes(self, uuid, username):
        key = str(generate_uuid())
        jwt_token = encode_token(name=username, sub=str(uuid), iss=key)
        return {
            'token': jwt_token.decode(),
            'status': 'active',
            'user_uuid': uuid
        }
