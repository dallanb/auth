import pytest

from src import services, app
from src.common import generate_expiry


@pytest.fixture
def seed_refresh_token():
    refresh_expiry = generate_expiry(app.config['REFRESH_EXP'])
    attr = services.RefreshToken().generate_token_attributes(uuid=pytest.user.uuid, username=pytest.user.username,
                                                             expiry=refresh_expiry)
    pytest.refresh_token = services.RefreshToken().create(**attr)
