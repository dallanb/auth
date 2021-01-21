from sqlalchemy_utils import UUIDType

from .mixins import BaseMixin, KongMixin
from .. import db
from ..common.enums import TokenStatusEnum
from ..common.utils import generate_token


class RefreshToken(db.Model, BaseMixin, KongMixin):
    token = db.Column(db.String, unique=True, nullable=False, default=generate_token)

    # FK
    user_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('user.uuid'), nullable=False)
    status = db.Column(db.Enum(TokenStatusEnum), db.ForeignKey('token_status.name'), nullable=True)

    # Relationship
    user = db.relationship("User")
    token_status = db.relationship("TokenStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


RefreshToken.register()
