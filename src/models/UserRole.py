from ..common import UserRoleEnum
from .. import db
from .mixins import EnumMixin


class UserRole(db.Model, EnumMixin):
    name = db.Column(db.Enum(UserRoleEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


UserRole.register()
