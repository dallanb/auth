from http import HTTPStatus


class ManualException(Exception):
    def __init__(self, code=HTTPStatus.INTERNAL_SERVER_ERROR.value, msg=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                 data=None, err=None):
        Exception.__init__(self)
        self.code = code
        self.msg = msg
        self.err = err
        self.data = data

    def to_dict(self):
        rv = dict(())
        rv['msg'] = self.msg
        rv['code'] = self.code
        rv['err'] = self.err
        return rv


class MissingParamError(ValueError):
    def __init__(self, key):
        self.message = f"Missing param: {key}"
        super().__init__(self.message)


class InvalidTypeError(TypeError):
    def __init__(self, key, key_type):
        self.message = f"Invalid type: {key} must be of type {key_type}"
        super().__init__(self.message)


class InvalidParamError(ValueError):
    def __init__(self, key):
        self.message = f"Invalid param: {key}"
        super().__init__(self.message)


class MalformedRequestError(Exception):
    def __init__(self, key):
        self.message = f"Malformed request: {key}"
        super().__init__(self.message)
