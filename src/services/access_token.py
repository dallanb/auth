import logging

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
        return Base.find(self, model=self.access_token_model, **kwargs)

    def create(self, **kwargs):
        access_token = self.init(model=self.access_token_model, **kwargs)
        return self.save(instance=access_token)

    def generate_token_attributes(self, uuid, username):
        key = str(generate_uuid())
        jwt_credential = self.access_token_model().create_jwt_credential(username=username, key=key)
        jwt_token = encode_token(name=username, sub=str(uuid), iss=key)
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
