from flask import g
from flask_restful import Resource
from ...common import ManualException
from http import HTTPStatus


class Base(Resource):
    def __init__(self):
        self.logger = g.logger.getLogger(__name__)
        self.cache = g.cache
        self.db = g.db
        self.code = HTTPStatus

    @staticmethod
    def throw_error(http_code, **kwargs):
        if http_code is None:
            raise ManualException()
        code = http_code.value
        msg = kwargs.get('msg', http_code.phrase)
        raise ManualException(code=code, msg=msg)
