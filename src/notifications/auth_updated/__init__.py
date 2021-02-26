from .schema import AuthUpdatedSchema
from ..base import Base


class auth_updated(Base):
    key = 'auth_updated'
    schema = AuthUpdatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, user):
        data = cls.schema.dump({'user': user})
        return auth_updated(data=data)
