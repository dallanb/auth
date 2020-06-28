from huncho.services.auth.src import app
import logging


def test_ping():
    response = app.test_client().get('/ping')

    assert response.status_code == 200
    assert b'pong' in response.data
