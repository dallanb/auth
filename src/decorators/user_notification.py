from functools import wraps


class user_notification:
    def __init__(self, operation):
        self.operation = operation
        self.topic = 'auth'
        self._service = None

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            self.service = args[0]
            first_name = kwargs.pop('first_name', None)
            last_name = kwargs.pop('last_name', None)
            new_instance = f(*args, **kwargs)
            self.create(new_instance=new_instance, first_name=first_name, last_name=last_name)
            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def create(self, new_instance, first_name, last_name):
        key = 'auth_created'
        value = {
            'username': new_instance.username,
            'email': new_instance.email,
            'uuid': str(new_instance.uuid),
            'first_name': first_name,
            'last_name': last_name
        }
        self.service.notify(topic=self.topic, value=value, key=key, )
