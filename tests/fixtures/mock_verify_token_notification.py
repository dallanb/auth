import pytest

from tests.helpers import verify_token_notification_create


@pytest.fixture
def mock_verify_token_notification_create(mocker):
    yield mocker.patch('src.decorators.notifications.verify_token_notification.create', verify_token_notification_create)

