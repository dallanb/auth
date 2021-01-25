import logging
from http import HTTPStatus

from .base import Base
from ..common.mail import Mail
from ..decorators import verify_token_notification
from ..models import VerifyToken as VerifyTokenModel


class VerifyToken(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.verify_token_model = VerifyTokenModel
        self.mail = Mail()

    def find(self, **kwargs):
        return Base.find(self, model=self.verify_token_model, **kwargs)

    @verify_token_notification(operation='create')
    def create(self, **kwargs):
        verify_token = self.init(model=self.verify_token_model, **kwargs)
        return self.save(instance=verify_token)

    def update(self, uuid, **kwargs):
        verify_tokens = self.find(uuid=uuid)
        if not verify_tokens.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=verify_tokens.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        verify_token = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=verify_token)

    def deactivate_tokens(self, email):
        self.db.clean_query(model=self.verify_token_model, email=email, status='active').update(
            {self.verify_token_model.status: 'inactive'}, synchronize_session=False)
        self.db.commit()
        return

    def send_verify(self, instance):
        subject = 'Tech Tapir Verification'
        body = self.mail.generate_body('verify', verify=instance)
        self.mail.send(to=instance.email, subject=subject, html=body)
