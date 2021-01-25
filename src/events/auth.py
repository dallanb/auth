import logging

from ..services import InviteToken as InviteTokenService, VerifyToken as VerifyTokenService, User as UserService


class Auth:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.invite_token_service = InviteTokenService()
        self.verify_token_service = VerifyTokenService()
        self.user_service = UserService()

    def handle_event(self, key, data):
        if key == 'auth_created':
            self.logger.info('auth created')
            # deactivate all invite tokens with this users email
            if data['status'] == 'active':
                self.invite_token_service.deactivate_tokens(email=data['email'])
            # if the user status is pending we should send a verification email
            elif data['status'] == 'pending':
                self.verify_token_service.create(email=data['email'], status='active')
