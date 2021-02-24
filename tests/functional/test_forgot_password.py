import json

import pytest

from src import app


def test_forgot_password(reset_db, pause_notification, seed_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'forgot_password' is requested
    THEN check that the response is valid
    """
    # Payload
    payload = {'email': pytest.email}

    # Request
    response = app.test_client().post('/forgot_password', json=payload)

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
