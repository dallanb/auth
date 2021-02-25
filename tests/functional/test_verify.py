import json

import pytest

from src import app


def test_verify(reset_db, pause_notification, seed_user, seed_verify_token):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'verify' is requested
    THEN check that the response is valid
    """
    # Payload
    payload = {'token': pytest.verify_token.token}

    # Request
    response = app.test_client().post('/verify', json=payload)

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
