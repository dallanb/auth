from .schema import AuthCreatedSchema
from ..base import Base


class auth_created(Base):
    key = 'auth_created'
    schema = AuthCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, user, display_name, country):
        data = cls.schema.dump({'user': user, 'display_name': display_name, 'country': country})
        return auth_created(data=data)
