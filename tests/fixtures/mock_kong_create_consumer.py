import pytest

from tests.helpers import kong_create_consumer


@pytest.fixture
def mock_kong_create_consumer(mocker):
    yield mocker.patch('src.models.mixins.KongMixin.create_consumer', kong_create_consumer)
