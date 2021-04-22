import pytest

from tests.helpers import reset_password_token_notification_create


@pytest.fixture
def mock_reset_password_token_notification_create(mocker):
    yield mocker.patch('src.decorators.notifications.reset_password_token_notification.create', reset_password_token_notification_create)

