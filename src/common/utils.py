import datetime
import uuid
from time import time

import jwt

from .. import app


def time_now():
    return int(time() * 1000.0)


def generate_uuid():
    return uuid.uuid4()


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def encode_token(**kwargs):
    exp = kwargs.get('exp', datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=30))
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
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )
    return token


def decode_token(token):
    try:
        return jwt.decode(token, app.config.get('SECRET_KEY'))
    except jwt.ExpiredSignatureError:
        raise ValueError('Signature expired. Please log in again.', 'destroy_token')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token. Please log in again.')
    except Exception as e:
        raise ValueError('Unknown error')
