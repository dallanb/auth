from ..common import UserRoleEnum
from .. import db
from .mixins import BaseMixin


class UserRole(db.Model, BaseMixin):
    name = db.Column(db.Enum(UserRoleEnum), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


UserRole.register()
