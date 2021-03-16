import pytest

from src import events, services


def test_member_member_invited_sync(reset_db, pause_notification, mock_kong_create_jwt_credential):
    """
    GIVEN 0 user instance in the database
    WHEN directly calling event auth handle_event auth_created
    THEN it should add 1 user instance to the database
    """
    key = 'member_invited'
    value = {
        'email': pytest.email,
    }

    events.Member().handle_event(key=key, data=value)

    invite_tokens = services.InviteToken().find()

    assert invite_tokens.total == 1
    invite_token = invite_tokens.items[0]
    assert str(invite_token.email) == value['email']
