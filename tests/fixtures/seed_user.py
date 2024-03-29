import pytest

from src import services


@pytest.fixture
def seed_user(mock_kong_create_consumer):
    pytest.user = services.User().create(username=pytest.username, email=pytest.email, password=pytest.password,
                                         display_name=pytest.display_name, country=pytest.country, role='member',
                                         status='active')
