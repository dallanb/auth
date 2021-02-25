import pytest


def kong_create_jwt_credential(self, username, key):
    return {'id': pytest.kong_jwt_id}
