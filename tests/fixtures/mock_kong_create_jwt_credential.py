import pytest

from tests.helpers import kong_create_jwt_credential


@pytest.fixture
def mock_kong_create_jwt_credential(mocker):
    yield mocker.patch('src.models.mixins.KongMixin.create_jwt_credential', kong_create_jwt_credential)
