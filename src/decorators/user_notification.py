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
            display_name = kwargs.pop('display_name', None)
            country = kwargs.pop('country', None)
            new_instance = f(*args, **kwargs)
            self.create(new_instance=new_instance, display_name=display_name, country=country)
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

    def create(self, new_instance, display_name, country):
        key = 'auth_created'
        value = {
            'username': new_instance.username,
            'email': new_instance.email,
            'uuid': str(new_instance.uuid),
            'display_name': display_name,
            'country': country
        }
        self.service.notify(topic=self.topic, value=value, key=key, )
