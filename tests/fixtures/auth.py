import json

import pytest

from src import app


@pytest.fixture
def auth(pause_notification):
    payload = {
        'email': pytest.email,
        'password': pytest.password,
    }
    response = app.test_client().post('/login', json=payload)
    response = json.loads(response.data)
    pytest.token = response['data']['access_token']
