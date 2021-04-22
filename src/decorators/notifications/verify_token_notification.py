from functools import wraps

from src import services
from src.notifications import verify_token_created


class verify_token_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            new_instance = f(*args, **kwargs)
            self.create(new_instance=new_instance)
            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @staticmethod
    def create(new_instance):
        verify_token_created.from_data(verify_token=new_instance).notify()
        services.VerifyToken().send_verify(instance=new_instance)
