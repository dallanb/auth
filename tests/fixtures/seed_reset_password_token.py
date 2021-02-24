import pytest

from src import services


@pytest.fixture
def seed_reset_password_token():
    pytest.reset_password_token = services.ResetPasswordToken().create(email=pytest.email, status='active')
