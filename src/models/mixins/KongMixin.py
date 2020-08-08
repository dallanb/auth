from sqlalchemy.event import listen
from ...external import Kong


class KongMixin(object):
    @staticmethod
    def create_consumer(uuid, username):
        return Kong().create_consumer(uuid=str(uuid), username=username)

    @staticmethod
    def create_jwt_credential(username, key):
        return Kong().create_jwt_credential(username=username, key=key, algorithm='HS256')

    @staticmethod
    def destroy_jwt_credential(username, jwt_id):
        return Kong().delete_jwt_credential(username=username, jwt_id=jwt_id)

    @classmethod
    def after_insert(cls, mapper, connection, target):
        cls.create_consumer(uuid=target.uuid, username=target.username)

    @classmethod
    def register_kong(cls):
        listen(cls, 'after_insert', cls.after_insert)
