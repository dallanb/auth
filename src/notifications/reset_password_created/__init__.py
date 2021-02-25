from .schema import ResetPasswordCreatedSchema
from ..base import Base


class reset_password_created(Base):
    key = 'reset_password_created'
    schema = ResetPasswordCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, reset_password):
        data = cls.schema.dump({'reset_password': reset_password})
        return reset_password_created(data=data)
