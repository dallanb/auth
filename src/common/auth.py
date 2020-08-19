from flask import g, request
from functools import wraps
from http import HTTPStatus
from .cleaner import Cleaner
from .error import ManualException


def check_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        consumer_id = request.headers.get('X-Consumer-Custom-ID', None)
        g.user = Cleaner.is_uuid(consumer_id)
        if not g.user:
            raise ManualException(code=HTTPStatus.UNAUTHORIZED.value, msg=HTTPStatus.UNAUTHORIZED.phrase)
        return f(*args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
