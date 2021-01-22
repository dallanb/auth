from sqlalchemy_utils import EmailType

from .mixins import BaseMixin
from .. import db
from ..common.enums import TokenStatusEnum


class InviteToken(db.Model, BaseMixin):
    token = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(EmailType, unique=False, nullable=False)

    # FK
    status = db.Column(db.Enum(TokenStatusEnum), db.ForeignKey('token_status.name'), nullable=True)

    # Relationship
    token_status = db.relationship("TokenStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


InviteToken.register()
