from http import HTTPStatus


class ManualException(Exception):
    def __init__(self, code=HTTPStatus.INTERNAL_SERVER_ERROR.value, msg=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                 data=False):
        Exception.__init__(self)
        self.code = code
        self.msg = msg
        self.data = data

    def to_dict(self):
        rv = dict(())
        rv['msg'] = self.msg
        rv['code'] = self.code
        return rv
