import json

import pytest

from src import app


def test_invite(reset_db, pause_notification, seed_user, seed_invite_token):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'invite' is requested
    THEN check that the response is valid
    """

    # Request
    response = app.test_client().get(f'/invites/token/{pytest.invite_token.token}')

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
