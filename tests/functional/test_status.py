import json

import pytest

from src import app


def test_status(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user, auth):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'status' is requested
    THEN check that the response is valid
    """
    # Headers
    headers = {'Authorization': f'Bearer {pytest.token}'}

    response = app.test_client().get('/status', headers=headers)

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
    assert response['data']['expiry'] is not None


def test_status_fail(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user, auth):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'status' is requested
    THEN check that the response is valid
    """
    response = app.test_client().get('/status')

    assert response.status_code == 401
