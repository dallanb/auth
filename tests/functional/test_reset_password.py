import json

import pytest

from src import app


def test_reset_password(reset_db, pause_notification, seed_user, seed_reset_password_token):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'reset_password' is requested
    THEN check that the response is valid
    """
    # Payload
    payload = {'token': pytest.reset_password_token.token, 'password': '1234'}

    # Request
    response = app.test_client().post('/reset_password', json=payload)

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
