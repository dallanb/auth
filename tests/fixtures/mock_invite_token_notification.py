import pytest

from tests.helpers import invite_token_notification_create


@pytest.fixture
def mock_invite_token_notification_create(mocker):
    yield mocker.patch('src.decorators.invite_token_notification.create', invite_token_notification_create)

