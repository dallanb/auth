import pytest

from src import app


def test_register(reset_db, pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'register' is requested
    THEN check that the response is valid
    """

    # Payload
    payload = {
        'email': pytest.email,
        'username': pytest.username,
        'password': pytest.password,
        'display_name': pytest.display_name,
        'country': pytest.country
    }

    response = app.test_client().post('/register', json=payload)

    assert response.status_code == 200


def test_register_fail(reset_db, pause_notification):
    """
    GIVEN a Flask application configured for testing
    WHEN the POST endpoint 'register' is requested
    THEN check that the response is valid
    """

    # Payload
    payload = {
        'email': pytest.username,
        'username': pytest.email,
        'password': pytest.password,
        'display_name': pytest.display_name,
        'country': pytest.country
    }

    response = app.test_client().post('/register', json=payload)

    assert response.status_code == 400
