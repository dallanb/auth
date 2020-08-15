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
        _ = self.notify(topic='auth', value=user.uuid, key='account_created')
        return self.save(instance=user)

    def send_register_mail(self, user):
        try:
            html = self.mail.generate_body('register', user=user)
            self.mail.send(
                to=user['email'],
                subject='Tech Tapir Registration',
                html=html
            )
        except Exception as e:
            raise ManualException(code=HTTPStatus.NOT_FOUND.value, msg=HTTPStatus.NOT_FOUND.phrase)
