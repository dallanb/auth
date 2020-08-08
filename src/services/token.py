import datetime
import jwt
from flask import g
from ..models import Token
from ..common.utils import generate_uuid


def generate_token_attributes(uuid, username):
    key = str(generate_uuid())
    jwt_credential = Token().create_jwt_credential(username=username, key=key)
    jwt_token = encode_token(name=username, sub=str(uuid), iss=key)
    return {
        'token': jwt_token.decode(),
        'kong_jwt_id': jwt_credential['id'],
        'status': 'active',
        'user_uuid': uuid
    }


def generate_deactivate_token_attributes(username, kong_jwt_id):
    _ = Token().destroy_jwt_credential(username=username, jwt_id=kong_jwt_id)
    return {
        'status': 'inactive',
        'kong_jwt_id': None
    }


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


def decode_token(token):
    try:
        return jwt.decode(token, g.config.get('SECRET_KEY'))
    except jwt.ExpiredSignatureError:
        raise ValueError('Signature expired. Please log in again.', 'destroy_token')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token. Please log in again.')
    except Exception as e:
        raise ValueError('Unknown error')
