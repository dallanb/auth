import base64, json, pickle
from sqlalchemy.event import listen
from ...proxy import KongProxy


class KongMixin(object):
    @staticmethod
    def create_consumer(uuid, username):
        return KongProxy().create_consumer(uuid=str(uuid), username=username)

    @staticmethod
    def create_jwt_credential(username, key):
        return KongProxy().create_jwt_credential(username=username, key=key, algorithm='HS256')

    @staticmethod
    def destroy_jwt_credential(username, jwt_id):
        return KongProxy().delete_jwt_credential(username=username, jwt_id=jwt_id)

    @classmethod
    def after_insert(cls, mapper, connection, target):
        cls.create_consumer(uuid=target.uuid, username=target.username)

    @classmethod
    def register_kong(cls):
        listen(cls, 'after_insert', cls.after_insert)
