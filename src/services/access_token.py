import logging
from http import HTTPStatus

from .base import Base
from ..common.mail import Mail
from ..common.utils import generate_uuid, encode_token
from ..models import AccessToken as AccessTokenModel


class AccessToken(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.access_token_model = AccessTokenModel
        self.mail = Mail()

    def find(self, **kwargs):
        return self._find(model=self.access_token_model, **kwargs)

    def create(self, **kwargs):
        access_token = self._init(model=self.access_token_model, **kwargs)
        return self._save(instance=access_token)

    def update(self, uuid, **kwargs):
        access_tokens = self.find(uuid=uuid)
        if not access_tokens.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=access_tokens.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        access_token = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=access_token)

    def generate_token_attributes(self, uuid, username, expiry):
        key = str(generate_uuid())
        jwt_credential = self.access_token_model().create_jwt_credential(username=username, key=key)
        jwt_token = encode_token(name=username, sub=str(uuid), iss=key, exp=expiry)
        return {
            'token': jwt_token.decode(),
            'kong_jwt_id': jwt_credential['id'],
            'status': 'active',
            'user_uuid': uuid
        }

    def generate_deactivate_token_attributes(self, username, kong_jwt_id):
        _ = self.access_token_model().destroy_jwt_credential(username=username, jwt_id=kong_jwt_id)
        return {
            'status': 'inactive',
            'kong_jwt_id': None
        }
