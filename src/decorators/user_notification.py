from functools import wraps

from src.notifications import auth_created, auth_updated


class user_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            display_name = kwargs.pop('display_name', None)
            country = kwargs.pop('country', None)
            new_instance = f(*args, **kwargs)
            if self.operation == 'create':
                self.create(new_instance=new_instance, display_name=display_name, country=country)
            if self.operation == 'update':
                self.update(new_instance=new_instance)
            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @staticmethod
    def create(new_instance, display_name, country):
        auth_created.from_data(user=new_instance, display_name=display_name, country=country).notify()

    @staticmethod
    def update(new_instance):
        auth_updated.from_data(user=new_instance).notify()
