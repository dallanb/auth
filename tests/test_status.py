from huncho.services.auth.src import app


def test_status():
    response = app.test_client().get('/status')

    assert response.status_code == 200
    assert b'user' in response.data
