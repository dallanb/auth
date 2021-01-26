from functools import wraps


class verify_token_notification:
    def __init__(self, operation):
        self.operation = operation
        self.topic = 'auth'
        self._service = None

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            self.service = args[0]
            new_instance = f(*args, **kwargs)
            self.create(new_instance=new_instance)
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

    def create(self, new_instance):
        key = 'verify_created'
        value = {
            'token': str(new_instance.token),
            'email': new_instance.email,
            'uuid': str(new_instance.uuid),
        }
        self.service.notify(topic=self.topic, value=value, key=key, )
        self.service.send_verify(instance=new_instance)
