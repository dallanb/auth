from .schema import InviteTokenCreatedSchema
from ..base import Base


class invite_token_created(Base):
    key = 'invite_token_created'
    schema = InviteTokenCreatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, invite_token):
        data = cls.schema.dump({'invite_token': invite_token})
        return invite_token_created(data=data)
