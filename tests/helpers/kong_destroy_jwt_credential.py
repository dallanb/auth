import pytest


def kong_destroy_jwt_credential(self, username, jwt_id):
    if jwt_id == pytest.kong_jwt_id:
        return True
