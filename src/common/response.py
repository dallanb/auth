from abc import ABC, abstractmethod
from flask_restful import fields
from http import HTTPStatus


class Response(ABC):
    @abstractmethod
    def marshallable(self):
        pass


class MessageResponse(Response):
    def __init__(self, **kwargs):
        self.msg = HTTPStatus.OK.phrase
        self.data = {
            'message': kwargs.get('message', 'OK')
        }

    @staticmethod
    def marshallable():
        return {
            'msg': fields.String,
            'data': fields.Raw
        }


class DataResponse(Response):
    def __init__(self, **kwargs):
        self.msg = HTTPStatus.OK.phrase
        self.data = kwargs.get('data', None)

    @staticmethod
    def marshallable():
        return {
            'msg': fields.String,
            'data': fields.Raw
        }


class ErrorResponse(Response):
    def __init__(self, **kwargs):
        self.msg = kwargs.get('msg', HTTPStatus.INTERNAL_SERVER_ERROR.phrase)
        self.err = kwargs.get('err', None)
        self.data = kwargs.get('data', None)

    @staticmethod
    def marshallable():
        return {
            'msg': fields.String,
            'err': fields.Raw,
            'data': fields.Raw,
        }
