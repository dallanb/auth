from .schema import VerifyCreatedSchema
from ..base import Base


class verify_created(Base):
    key = 'verify_created'
    schema = VerifyCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, verify):
        data = cls.schema.dump({'verify': verify})
        return verify_created(data=data)
