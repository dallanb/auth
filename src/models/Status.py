from ..common import StatusEnum
from .. import db
from .mixins import BaseMixin


class Status(db.Model, BaseMixin):
    name = db.Column(db.Enum(StatusEnum), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Status.register()
