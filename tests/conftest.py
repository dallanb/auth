from uuid import uuid4

import pytest

from .fixtures import *
from .test_flaskr import client


def pytest_configure(config):
    pytest.user = None
    pytest.token = None
    pytest.access_token = None
    pytest.invite_token = None
    pytest.refresh_token = None
    pytest.reset_password_token = None
    pytest.token_status = None
    pytest.user_role = None
    pytest.user_status = None
    pytest.verify_token = None
    pytest.email = 'dallanbhatti@gmail.com'
    pytest.username = 'dallanbhatti'
    pytest.password = '123'
    pytest.display_name = 'Dallan Bhatti'
    pytest.country = 'CA'
    pytest.access_token_token = uuid4()
    pytest.kong_jwt_id = uuid4()
