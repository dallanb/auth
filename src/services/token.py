import datetime
import jwt
import logging
from flask import g

from .base import Base
from ..models import Token as TokenModel
from ..common.mail import Mail
from ..common.utils import generate_uuid


class Token(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.token_model = TokenModel
        self.mail = Mail()

    def find(self, **kwargs):
        return Base.find(self, model=self.token_model, **kwargs)

    def create(self, **kwargs):
        token = self.init(model=self.token_model, **kwargs)
        return self.save(instance=token)

    def generate_token_attributes(self, uuid, username):
        key = str(generate_uuid())
        jwt_credential = self.token_model().create_jwt_credential(username=username, key=key)
        jwt_token = self.encode_token(name=username, sub=str(uuid), iss=key)
        return {
            'token': jwt_token.decode(),
            'kong_jwt_id': jwt_credential['id'],
            'status': 'active',
            'user_uuid': uuid
        }

    def generate_deactivate_token_attributes(self, username, kong_jwt_id):
        _ = self.token_model().destroy_jwt_credential(username=username, jwt_id=kong_jwt_id)
        return {
            'status': 'inactive',
            'kong_jwt_id': None
        }

    @staticmethod
    def encode_token(**kwargs):
        exp = kwargs.get('exp', datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=300))
        iat = kwargs.get('iat', datetime.datetime.utcnow())
        name = kwargs.get('name', None)
        sub = kwargs.get('sub', None)
        iss = kwargs.get('iss', str(generate_uuid()))
        token = jwt.encode(
            {
                'exp': exp,
                'iat': iat,
                'name': name,
                'sub': sub,
                'iss': iss
            },
            g.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
        return token

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, g.config.get('SECRET_KEY'))
        except jwt.ExpiredSignatureError:
            raise ValueError('Signature expired. Please log in again.', 'destroy_token')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token. Please log in again.')
        except Exception as e:
            raise ValueError('Unknown error')
