from sqlalchemy_utils import EmailType, PasswordType, UUIDType
from .. import db
from .mixins import BaseMixin, KongMixin
from .UserRole import UserRole
from .UserStatus import UserStatus


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
    role_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('userrole.uuid'), nullable=True)
    status_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('userstatus.uuid'), nullable=True)

    # Relationship
    role = db.relationship("UserRole")
    status = db.relationship("UserStatus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_password(self, password):
        return self.password == password

    @staticmethod
    def find_role(role_enum=None):
        if role_enum is None:
            return None

        role = UserRole.query.filter(UserRole.name == role_enum).first()
        if role_enum is None:
            return None

        return role

    @staticmethod
    def find_status(status_enum=None):
        if status_enum is None:
            return None

        status = UserStatus.query.filter(UserStatus.name == status_enum).first()

        if status_enum is None:
            return None

        return status


User.register()
User.register_kong()
