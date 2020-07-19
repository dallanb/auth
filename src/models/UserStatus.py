from ..common import UserStatusEnum
from .. import db
from .mixins import BaseMixin


class UserStatus(db.Model, BaseMixin):
    name = db.Column(db.Enum(UserStatusEnum), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


UserStatus.register()
