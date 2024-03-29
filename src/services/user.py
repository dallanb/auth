import logging
from http import HTTPStatus

from .base import Base
from ..common.mail import Mail
from ..decorators.notifications import user_notification
from ..models import User as UserModel


class User(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.user_model = UserModel
        self.mail = Mail()

    def find(self, **kwargs):
        return self._find(model=self.user_model, **kwargs)

    @user_notification(operation='create')
    def create(self, **kwargs):
        user = self._init(model=self.user_model, **kwargs)
        return self._save(instance=user)

    def update(self, uuid, **kwargs):
        users = self.find(uuid=uuid)
        if not users.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=users.items[0], **kwargs)

    @user_notification(operation='update')
    def apply(self, instance, **kwargs):
        user = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=user)
