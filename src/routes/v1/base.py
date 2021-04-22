import logging
from http import HTTPStatus

from flask_restful import Resource
from marshmallow import ValidationError

from ... import app
from ...common.error import ManualException
from ...decorators import log_trace
from ...services import Base as Service


class Base(Resource):
    def __init__(self):
        self.service = Service()
        self.logger = logging.getLogger(__name__)
        self.code = HTTPStatus
        self.config = app.config

    def dump(self, schema, instance, params=None):
        return self.service.dump(schema=schema, instance=instance, params=params)

    def clean(self, schema, instance, **kwargs):
        try:
            return self.service.clean(schema=schema, instance=instance, **kwargs)
        except ValidationError as err:
            Base.throw_error(http_code=self.code.BAD_REQUEST, err=err.messages)

    @staticmethod
    @log_trace
    def throw_error(http_code, **kwargs):
        if http_code is None:
            raise ManualException()
        code = http_code.value
        msg = kwargs.get('msg', http_code.phrase)
        err = kwargs.get('err', None)
        raise ManualException(code=code, msg=msg, err=err)

    @staticmethod
    def prepare_metadata(total_count, page_count, page, per_page):
        return {
            'total_count': total_count,
            'page_count': page_count,
            'page': page,
            'per_page': per_page
        }
