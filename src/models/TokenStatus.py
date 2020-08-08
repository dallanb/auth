from ..common import TokenStatusEnum
from .. import db
from .mixins import EnumMixin


class TokenStatus(db.Model, EnumMixin):
    name = db.Column(db.Enum(TokenStatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


TokenStatus.register()
