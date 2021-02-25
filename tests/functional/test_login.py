import pytest

from src import app


def test_login(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'login' is requested
    THEN check that the response is valid
    """

    # Payload
    payload = {
        'email': pytest.email,
        'password': pytest.password,
    }

    response = app.test_client().post('/login', json=payload)

    assert response.status_code == 200


def test_login_fail(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'login' is requested
    THEN check that the response is valid
    """

    # Payload
    payload = {
        'username': pytest.username,
        'password': pytest.password,
    }

    response = app.test_client().post('/login', json=payload)

    assert response.status_code == 400
