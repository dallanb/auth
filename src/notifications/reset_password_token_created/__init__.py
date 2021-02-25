from .schema import ResetPasswordCreatedSchema
from ..base import Base


class reset_password_token_created(Base):
    key = 'reset_password_token_created'
    schema = ResetPasswordCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, reset_password_token):
        data = cls.schema.dump({'reset_password_token': reset_password_token})
        return reset_password_token_created(data=data)
