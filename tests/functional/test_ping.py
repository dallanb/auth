from src import app


def test_ping(client):
    response = app.test_client().get('/ping')

    assert response.status_code == 200
    assert b'pong' in response.data
