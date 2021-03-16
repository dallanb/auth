import pytest

from src import services, app
from src.common import generate_expiry


@pytest.fixture
def seed_access_token():
    access_expiry = generate_expiry(app.config['ACCESS_EXP'])
    attr = services.AccessToken().generate_token_attributes(uuid=pytest.user.uuid, username=pytest.user.username,
                                                            expiry=access_expiry)
    pytest.access_token = services.AccessToken().create(**attr, refresh_token=pytest.refresh_token)
