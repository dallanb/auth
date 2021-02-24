import pytest


@pytest.fixture(scope="function")
def pause_notification(mock_user_notification_create, mock_user_notification_update,
                       mock_invite_token_notification_create, mock_reset_password_token_notification_create,
                       mock_verify_token_notification_create):
    return True
