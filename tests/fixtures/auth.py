import json

import pytest

from src import app


@pytest.fixture
def auth(pause_notification, mock_kong_create_jwt_credential):
    payload = {
        'email': pytest.email,
        'password': pytest.password,
    }
    response = app.test_client().post('/login', json=payload)
    cookie = response.headers['Set-Cookie']
    _, pytest.refresh_token = cookie.split('=')
    response = json.loads(response.data)
    pytest.token = response['data']['access_token']
