import logging
from http import HTTPStatus

from .base import Base
from ..common.mail import Mail
from ..decorators import invite_token_notification
from ..models import InviteToken as InviteTokenModel


class InviteToken(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.invite_token_model = InviteTokenModel
        self.mail = Mail()

    def find(self, **kwargs):
        return Base.find(self, model=self.invite_token_model, **kwargs)

    @invite_token_notification(operation='create')
    def create(self, **kwargs):
        invite_token = self.init(model=self.invite_token_model, **kwargs)
        return self.save(instance=invite_token)

    def update(self, uuid, **kwargs):
        invite_tokens = self.find(uuid=uuid)
        if not invite_tokens.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=invite_tokens.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        invite_token = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=invite_token)

    def deactivate_tokens(self, email):
        query = self.db.clean_query(model=self.invite_token_model, email=email, status='active')
        query.update(status='inactive')
        return self.db.run_query(query=query)

    def send_invite(self, instance):
        subject = 'Tech Tapir Invitation'
        body = self.mail.generate_body('invite', invite=instance)
        self.logger.info(body)
        # self.mail.send(to=instance.email, subject=subject, html=body)
