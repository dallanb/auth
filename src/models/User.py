import datetime, jwt
from flask import g
from sqlalchemy.event import listens_for
from sqlalchemy_utils import EmailType, PasswordType, UUIDType
from .. import db, ma
from .Base import Base
from .BlacklistToken import BlacklistToken
from .Role import Role
from .Status import Status
from .utils import generate_uuid


class User(Base):
    __tablename__ = 'user'
    uuid = db.Column(UUIDType(binary=False), unique=True, nullable=False)
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
    role_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('role.uuid'), nullable=True)
    status_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('status.uuid'), nullable=True)

    # Relationship
    role = db.relationship("Role")
    status = db.relationship("Status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_password(self, password):
        return self.password == password

    @staticmethod
    def find_role(role_enum=None):
        if role_enum is None:
            return None

        role = Role.query.filter(Role.name == role_enum).first()
        if role_enum is None:
            return None

        return role

    @staticmethod
    def find_status(status_enum=None):
        if status_enum is None:
            return None

        status = Status.query.filter(Status.name == status_enum).first()

        if status_enum is None:
            return None

        return status

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=300),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                g.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, g.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


@listens_for(User, 'before_insert')
def before_insert(mapper, connect, self):
    self.uuid = generate_uuid()


@listens_for(User, 'before_update')
def before_update(mapper, connect, self):
    return


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    uuid = ma.auto_field()
    email = ma.auto_field()
    username = ma.auto_field()
    role_uuid = ma.auto_field()
    status_uuid = ma.auto_field()
