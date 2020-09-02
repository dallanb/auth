from sqlalchemy_utils import UUIDType
from .mixins import BaseMixin, KongMixin
from .. import db
from ..common.enums import TokenStatusEnum


class AccessToken(db.Model, BaseMixin, KongMixin):
    token = db.Column(db.String, unique=True, nullable=False)
    kong_jwt_id = db.Column(UUIDType(binary=False), unique=False, nullable=True)

    # FK
    user_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('user.uuid'), nullable=False)
    status = db.Column(db.Enum(TokenStatusEnum), db.ForeignKey('token_status.name'), nullable=True)

    # Relationship
    user = db.relationship("User")
    token_status = db.relationship("TokenStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


AccessToken.register()
