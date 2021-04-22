import inspect
import logging
from functools import wraps


def log_trace(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        stack = inspect.stack()
        logging.error(f'log trace: {stack[1][0]}')
        return f(*args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
