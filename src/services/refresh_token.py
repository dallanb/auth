import datetime
import logging
from http import HTTPStatus

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
        return self._find(model=self.refresh_token_model, **kwargs)

    def create(self, **kwargs):
        refresh_token = self._init(model=self.refresh_token_model, **kwargs)
        return self._save(instance=refresh_token)

    def update(self, uuid, **kwargs):
        refresh_tokens = self.find(uuid=uuid)
        if not refresh_tokens.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=refresh_tokens.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        refresh_token = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=refresh_token)

    @staticmethod
    def generate_token_attributes(uuid, username, expiry):
        key = str(generate_uuid())
        jwt_token = encode_token(name=username, sub=str(uuid), iss=key,
                                 exp=expiry)
        return {
            'token': jwt_token.decode(),
            'status': 'active',
            'user_uuid': uuid
        }
