from ..common import RoleEnum
from .. import db
from .mixins import BaseMixin


class Role(db.Model, BaseMixin):
    name = db.Column(db.Enum(RoleEnum), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Role.register()
