from functools import wraps

from src import services
from src.notifications import reset_password_token_created


class reset_password_token_notification:
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
        reset_password_token_created.from_data(reset_password_token=new_instance).notify()
        services.ResetPasswordToken().send_reset_password(instance=new_instance)
