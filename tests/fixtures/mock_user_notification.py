import pytest

from tests.helpers import user_notification_create, user_notification_update


@pytest.fixture
def mock_user_notification_create(mocker):
    yield mocker.patch('src.decorators.user_notification.create', user_notification_create)


@pytest.fixture
def mock_user_notification_update(mocker):
    yield mocker.patch('src.decorators.user_notification.update', user_notification_update)
