from ..common import UserStatusEnum
from .. import db
from .mixins import EnumMixin


class UserStatus(db.Model, EnumMixin):
    name = db.Column(db.Enum(UserStatusEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


UserStatus.register()
