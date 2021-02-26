import pytest

from src import services


@pytest.fixture
def seed_invite_token():
    pytest.invite_token = services.InviteToken().create(email=pytest.email, status='active')
