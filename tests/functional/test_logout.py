import json

import pytest

from src import app


def test_logout(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user, auth):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'logout' is requested
    THEN check that the response is valid
    """
    # Headers
    headers = {'Authorization': f'Bearer {pytest.token}'}

    response = app.test_client().post('/logout', headers=headers)

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"


def test_logout_fail(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user, auth):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'logout' is requested
    THEN check that the response is valid
    """
    response = app.test_client().post('/logout')

    assert response.status_code == 401
