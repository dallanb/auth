import pytest

from src import events, services
from tests.helpers import generate_uuid


def test_auth_auth_created_sync(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user):
    """
    GIVEN 0 user instance  in the database
    WHEN directly calling event auth handle_event auth_created
    THEN it should add 1 user instance to the database
    """
    key = 'auth_created'
    value = {
        'username': pytest.username,
        'email': pytest.email,
        'uuid': str(pytest.user.uuid),
        'display_name': pytest.display_name,
        'country': pytest.country,
        'status': 'pending'
    }

    events.Auth().handle_event(key=key, data=value)

    users = services.User().find()

    assert users.total == 1
    user = users.items[0]
    assert str(user.uuid) == value['uuid']


def test_auth_auth_updated_sync(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user):
    """
    GIVEN 1 user instance in the database
    WHEN directly calling event auth handle_event auth_updated
    THEN it should add 1 user instance instance to the database
    """
    key = 'auth_created'
    value = {
        'username': pytest.username,
        'email': pytest.email,
        'uuid': str(pytest.user.uuid),
        'display_name': pytest.display_name,
        'country': pytest.country,
        'status': 'pending'
    }

    events.Auth().handle_event(key=key, data=value)

    users = services.User().find()

    assert users.total == 1
    user = users.items[0]
    assert str(user.uuid) == value['uuid']
