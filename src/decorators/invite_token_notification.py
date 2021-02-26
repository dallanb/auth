from functools import wraps

from src import services
from src.notifications import invite_token_created


class invite_token_notification:
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
        invite_token_created.from_data(invite_token=new_instance).notify()
        services.InviteToken().send_invite(instance=new_instance)
