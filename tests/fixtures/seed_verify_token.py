import pytest

from src import services


@pytest.fixture
def seed_verify_token():
    pytest.verify_token = services.VerifyToken().create(email=pytest.email, status='active')
