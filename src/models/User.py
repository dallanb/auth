from sqlalchemy_utils import EmailType, PasswordType, UUIDType
from .mixins import BaseMixin, KongMixin
from .. import db
from ..common import UserStatusEnum, UserRoleEnum


class User(db.Model, BaseMixin, KongMixin):
    email = db.Column(EmailType, unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(PasswordType(
        max_length=1137,
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt'],
    ))

    # FK
    role = db.Column(db.Enum(UserRoleEnum), db.ForeignKey('user_role.name'), nullable=True)
    status = db.Column(db.Enum(UserStatusEnum), db.ForeignKey('user_status.name'), nullable=True)

    # Relationship
    user_role = db.relationship("UserRole")
    user_status = db.relationship("UserStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


User.register()
User.register_kong()
