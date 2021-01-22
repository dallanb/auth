import logging

from ..services import InviteToken as InviteTokenService, User as UserService


class Auth:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.invite_token_service = InviteTokenService()
        self.user_service = UserService()

    def handle_event(self, key, data):
        if key == 'auth_created':
            self.logger.info('auth created')
            # deactivate all invite tokens with this users email
            self.invite_token_service.deactivate_tokens(email=data['email'])
