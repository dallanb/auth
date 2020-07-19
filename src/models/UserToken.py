import datetime, jwt
from flask import g
from sqlalchemy_utils import UUIDType
from ..common import UserTokenStatusEnum
from .. import db
from .mixins import BaseMixin, KongMixin
from .utils import generate_uuid
from .User import User


class UserToken(db.Model, BaseMixin, KongMixin):
    token = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.Enum(UserTokenStatusEnum), nullable=False)
    kong_jwt_id = db.Column(UUIDType(binary=False), unique=False, nullable=True)

    # FK
    user_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('user.uuid'), nullable=False)

    # Relationship
    user = db.relationship("User")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @classmethod
    def create_auth_token(cls, uuid, username):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            key = str(generate_uuid())

            jwt_credential = cls.create_jwt_credential(username=username, key=key)

            jwt_token = cls.encode_token(
                name=username,
                sub=str(uuid),
                iss=key
            )

            user_token = UserToken(token=jwt_token.decode(), kong_jwt_id=jwt_credential['id'],
                                   status=UserTokenStatusEnum.active,
                                   user_uuid=uuid)
            db.session.add(user_token)
            db.session.commit()
            return user_token
        except Exception as e:
            return e

    @classmethod
    def destroy_auth_token(cls, auth_token):
        q = db.session.query(
            User, UserToken,
        ).filter(
            User.uuid == UserToken.user_uuid,
        ).filter(
            UserToken.token == str(auth_token),
        ).first()

        if not q:
            return False

        user = q[0]
        user_token = q[1]

        cls.destroy_jwt_credential(username=user.username, jwt_id=user_token.kong_jwt_id)

        user_token.status = UserTokenStatusEnum.inactive
        user_token.kong_jwt_id = None

        db.session.commit()
        return True

    @staticmethod
    def encode_token(**kwargs):
        exp = kwargs.get('exp', datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=300))
        iat = kwargs.get('iat', datetime.datetime.utcnow())
        name = kwargs.get('name', None)
        sub = kwargs.get('sub', None)
        iss = kwargs.get('iss', str(generate_uuid()))
        token = jwt.encode(
            {
                'exp': exp,
                'iat': iat,
                'name': name,
                'sub': sub,
                'iss': iss
            },
            g.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
        return token

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, g.config.get('SECRET_KEY'))
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def is_active(token):
        # check whether auth token is active
        res = UserToken.query.filter(UserToken.token == str(token),
                                     UserToken.status == UserTokenStatusEnum.active).first()
        if res:
            return True
        else:
            return False


UserToken.register()
