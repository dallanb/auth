from .schema import VerifyTokenCreatedSchema
from ..base import Base


class verify_token_created(Base):
    key = 'verify_token_created'
    schema = VerifyTokenCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, verify_token):
        data = cls.schema.dump({'verify_token': verify_token})
        return verify_token_created(data=data)
