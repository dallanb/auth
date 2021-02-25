from .schema import InviteCreatedSchema
from ..base import Base


class invite_created(Base):
    key = 'invite_created'
    schema = InviteCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, invite_token):
        data = cls.schema.dump({'invite_token': invite_token})
        return invite_created(data=data)
