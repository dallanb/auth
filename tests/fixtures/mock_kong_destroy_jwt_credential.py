import pytest

from tests.helpers import kong_destroy_jwt_credential


@pytest.fixture
def mock_kong_destroy_jwt_credential(mocker):
    yield mocker.patch('src.models.mixins.KongMixin.destroy_jwt_credential', kong_destroy_jwt_credential)
