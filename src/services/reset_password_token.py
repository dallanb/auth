import logging
from http import HTTPStatus


from .base import Base
from ..common.mail import Mail
from ..decorators.notifications import reset_password_token_notification
from ..models import ResetPasswordToken as ResetPasswordTokenModel


class ResetPasswordToken(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.reset_password_token_model = ResetPasswordTokenModel
        self.mail = Mail()

    def find(self, **kwargs):
        return self._find(model=self.reset_password_token_model, **kwargs)

    @reset_password_token_notification(operation='create')
    def create(self, **kwargs):
        reset_password_token = self._init(model=self.reset_password_token_model, **kwargs)
        return self._save(instance=reset_password_token)

    def update(self, uuid, **kwargs):
        reset_password_tokens = self.find(uuid=uuid)
        if not reset_password_tokens.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=reset_password_tokens.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        reset_password_token = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=reset_password_token)

    def deactivate_tokens(self, email):
        self.db.clean_query(model=self.reset_password_token_model, email=email, status='active').update(
            {self.reset_password_token_model.status: 'inactive'}, synchronize_session=False)
        self.db.commit()
        return

    def send_reset_password(self, instance):
        subject = 'Tech Tapir Reset Password'
        body = self.mail.generate_body('reset_password', reset_password=instance, config=self.config)
        self.mail.send(to=instance.email, subject=subject, html=body)
