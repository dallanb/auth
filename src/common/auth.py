from flask import g, request
from functools import wraps
from http import HTTPStatus
from .error import ManualException


def check_auth(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            g.auth = request.headers.get('Authorization', None)
            g.access_token = g.auth.split(" ")[1]
        except Exception:
            raise ManualException(code=HTTPStatus.UNAUTHORIZED.value, msg=HTTPStatus.UNAUTHORIZED.phrase)
        return f(*args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
