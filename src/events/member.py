import logging

from ..services import InviteToken as InviteTokenService, User as UserService


class Member:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.invite_token_service = InviteTokenService()
        self.user_service = UserService()

    def handle_event(self, key, data):
        if key == 'member_invited':
            self.logger.info('member invited')
            # check to see if we already have a user with the provided email
            users = self.user_service.find(email=data['email'])
            if not users.total:
                # set all existing tokens for this email to inactive
                self.invite_token_service.deactivate_tokens(email=data['email'])
                # create a new token with this email
                _ = self.invite_token_service.create(email=data['email'], status='active')
