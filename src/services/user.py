import logging

from .base import Base
from ..common.mail import Mail
from ..decorators import user_notification
from ..models import User as UserModel


class User(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.user_model = UserModel
        self.mail = Mail()

    def find(self, **kwargs):
        return Base.find(self, model=self.user_model, **kwargs)

    @user_notification(operation='create')
    def create(self, **kwargs):
        user = self.init(model=self.user_model, **kwargs)
        return self.save(instance=user)
