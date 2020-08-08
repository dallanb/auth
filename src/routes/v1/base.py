from flask import g
from flask_restful import Resource
from http import HTTPStatus
from marshmallow import ValidationError
from ...common.error import ManualException
from ...common.db import find, save, init, destroy, count


class Base(Resource):
    def __init__(self):
        self.logger = g.logger.getLogger(__name__)
        self.code = HTTPStatus

    @staticmethod
    def count(model):
        return count(model=model)

    @staticmethod
    def find(model, not_found=None, **kwargs):
        instance = find(model=model, **kwargs)
        if not instance.total and not_found:
            Base.throw_error(http_code=not_found)
        return instance

    @staticmethod
    def init(model, **kwargs):
        return init(model=model, **kwargs)

    @staticmethod
    def save(instance):
        return save(instance=instance)

    @staticmethod
    def destroy(instance):
        return destroy(instance=instance)

    @staticmethod
    def dump(schema, instance, params=None):
        if params:
            for k, v in params.items():
                schema.context[k] = v
        return schema.dump(instance)

    @staticmethod
    def clean(schema, instance, **kwargs):
        try:
            return schema.load(instance, **kwargs)
        except ValidationError as err:
            Base.throw_error(http_code=HTTPStatus.BAD_REQUEST, err=err.messages)

    @staticmethod
    def assign_attr(instance, attr):
        for k, v in attr.items():
            instance.__setattr__(k, v)
        return instance

    @staticmethod
    def throw_error(http_code, **kwargs):
        if http_code is None:
            raise ManualException()
        code = http_code.value
        msg = kwargs.get('msg', http_code.phrase)
        raise ManualException(code=code, msg=msg)
