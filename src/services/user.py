import logging
from http import HTTPStatus

from .base import Base
from ..models import User as UserModel
from ..common.mail import Mail
from ..common.error import ManualException


class User(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.user_model = UserModel
        self.mail = Mail()

    def find(self, **kwargs):
        return Base.find(self, model=self.user_model, **kwargs)

    def create(self, **kwargs):
        user = self.init(model=self.user_model, **kwargs)
        _ = self.notify(
            topic='auth',
            value={
                'username': user.username,
                'email': user.email,
                'uuid': str(user.uuid)
            },
            key='auth_created'
        )
        return self.save(instance=user)