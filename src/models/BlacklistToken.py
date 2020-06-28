from .. import db
from .mixins import BaseMixin


class BlacklistToken(db.Model, BaseMixin):
    """
    Token Model for storing JWT tokens
    """
    token = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


BlacklistToken.register()
