from marshmallow_enum import EnumField
from ... import ma
from ..Status import Status
from ...common import StatusEnum


class StatusSchema(ma.SQLAlchemySchema):
    name = EnumField(StatusEnum)

    class Meta:
        model = Status
        load_instance = True

    uuid = ma.auto_field()
