import json

import pytest

from src import app


def test_refresh(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user, auth):
    """
    GIVEN a Flask application configured for testing
    WHEN the GET endpoint 'refresh' is requested
    THEN check that the response is valid
    """
    # Headers
    headers = {'Authorization': f'Bearer {pytest.token}'}

    client = app.test_client()
    client.set_cookie('localhost', 'refresh_token', pytest.refresh_token)
    response = client.get('/refresh', headers=headers)

    assert response.status_code == 200
    response = json.loads(response.data)
    assert response['msg'] == "OK"
