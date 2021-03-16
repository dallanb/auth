import pytest

from src import services, ManualException, app
from src.common import generate_expiry
from tests.helpers import generate_uuid

access_token_service = services.AccessToken()


###########
# Find
###########
def test_access_token_find(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user, seed_refresh_token,
                           seed_access_token):
    """
    GIVEN 1 access_token instance in the database
    WHEN the find method is called
    THEN it should return 1 access_token
    """

    access_tokens = access_token_service.find()
    assert access_tokens.total == 1
    assert len(access_tokens.items) == 1
    access_token = access_tokens.items[0]
    assert access_token.uuid == pytest.access_token.uuid


def test_access_token_find_by_uuid():
    """
    GIVEN 1 access_token instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 access_token
    """
    access_token = pytest.access_token
    uuid = access_token.uuid

    access_tokens = access_token_service.find(uuid=uuid)
    assert access_tokens.total == 1
    assert len(access_tokens.items) == 1
    access_token = access_tokens.items[0]
    assert access_token.uuid == uuid


def test_access_token_find_by_token():
    """
    GIVEN 1 access_token instance in the database
    WHEN the find method is called with token
    THEN it should return 1 access_token
    """
    access_token = pytest.access_token
    token = access_token.token

    access_tokens = access_token_service.find(token=token)
    assert access_tokens.total == 1
    assert len(access_tokens.items) == 1
    access_token = access_tokens.items[0]
    assert access_token.token == token


def test_access_token_find_w_pagination(pause_notification, mock_kong_create_jwt_credential, seed_access_token):
    """
    GIVEN 2 access_token instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of access_tokens defined in the pagination arguments
    """
    access_tokens_0 = access_token_service.find(page=1, per_page=1)
    assert access_tokens_0.total == 2
    assert len(access_tokens_0.items) == 1

    access_tokens_1 = access_token_service.find(page=2, per_page=1)
    assert access_tokens_1.total == 2
    assert len(access_tokens_1.items) == 1
    assert access_tokens_1.items[0] != access_tokens_0.items[0]

    access_tokens = access_token_service.find(page=1, per_page=2)
    assert access_tokens.total == 2
    assert len(access_tokens.items) == 2


def test_access_token_find_w_bad_pagination():
    """
    GIVEN 2 access_token instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 access_token
    """
    access_tokens = access_token_service.find(page=3, per_page=3)
    assert access_tokens.total == 2
    assert len(access_tokens.items) == 0


def test_access_token_find_by_token_none_found():
    """
    GIVEN 2 access_token instance in the database
    WHEN the find method is called with a random token
    THEN it should return the 0 access_token
    """
    access_tokens = access_token_service.find(token='123456')
    assert access_tokens.total == 0
    assert len(access_tokens.items) == 0


def test_access_token_find_by_non_existent_column():
    """
    GIVEN 2 access_token instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 access_token and ManualException with code 400
    """
    try:
        _ = access_token_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_access_token_find_by_non_existent_include():
    """
    GIVEN 2 access_token instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 access_token and ManualException with code 400
    """
    try:
        _ = access_token_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_access_token_find_by_non_existent_expand():
    """
    GIVEN 2 access_token instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 access_token and ManualException with code 400
    """
    try:
        _ = access_token_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_access_token_create(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                             seed_refresh_token):
    """
    GIVEN 0 access_token instance in the database
    WHEN the create method is called
    THEN it should return 1 access_token and add 1 access_token instance into the database
    """
    access_expiry = generate_expiry(app.config['ACCESS_EXP'])
    attr = services.AccessToken().generate_token_attributes(uuid=pytest.user.uuid, username=pytest.user.username,
                                                            expiry=access_expiry)
    access_token = access_token_service.create(**attr, refresh_token=pytest.refresh_token)

    assert access_token.uuid is not None
    assert access_token.token is not None


def test_access_token_create_dup(pause_notification, mock_kong_create_jwt_credential):
    """
    GIVEN 1 access_token instance in the database
    WHEN the create method is called with the exact same parameters of an existing access_token
    THEN it should return 1 access_token and add 1 access_token instance into the database
    """
    access_expiry = generate_expiry(app.config['ACCESS_EXP'])
    attr = services.AccessToken().generate_token_attributes(uuid=pytest.user.uuid, username=pytest.user.username,
                                                            expiry=access_expiry)
    access_token = access_token_service.create(**attr, refresh_token=pytest.refresh_token)
    assert access_token is not None


def test_access_token_create_w_bad_field(pause_notification, mock_kong_create_jwt_credential):
    """
    GIVEN 1 access_token instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 access_token and add 0 access_token instance into the database and ManualException with code 500
    """
    try:
        access_expiry = generate_expiry(app.config['ACCESS_EXP'])
        attr = services.AccessToken().generate_token_attributes(uuid=pytest.user.uuid, username=pytest.user.username,
                                                                expiry=access_expiry)
        _ = access_token_service.create(**attr, refresh_token=pytest.refresh_token, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_access_token_update(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                             seed_refresh_token, seed_access_token):
    """
    GIVEN 1 access_token instance in the database
    WHEN the update method is called
    THEN it should return 1 access_token and update 1 access_token instance into the database
    """
    access_token = access_token_service.update(uuid=pytest.access_token.uuid, status='inactive')
    assert access_token.uuid is not None

    access_tokens = access_token_service.find(uuid=access_token.uuid)
    assert access_tokens.total == 1
    assert len(access_tokens.items) == 1


def test_access_token_update_w_bad_uuid(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                                        seed_refresh_token, seed_access_token):
    """
    GIVEN 1 access_token instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 access_token and update 0 access_token instance into the database and ManualException with code 404
    """
    try:
        _ = access_token_service.update(uuid=generate_uuid(), status='inactive')
    except ManualException as ex:
        assert ex.code == 404


def test_access_token_update_w_bad_field(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                                         seed_refresh_token,
                                         seed_access_token):
    """
    GIVEN 1 access_token instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 access_token and update 0 access_token instance in the database and ManualException with code 400
    """
    try:
        _ = access_token_service.update(uuid=pytest.access_token.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_access_token_apply(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                            seed_refresh_token, seed_access_token):
    """
    GIVEN 1 access_token instance in the database
    WHEN the apply method is called
    THEN it should return 1 access_token and update 1 access_token instance in the database
    """
    access_token = access_token_service.apply(instance=pytest.access_token, status='inactive')
    assert access_token.uuid is not None

    access_tokens = access_token_service.find(uuid=access_token.uuid)
    assert access_tokens.total == 1
    assert len(access_tokens.items) == 1


def test_access_token_apply_w_bad_access_token(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                                               seed_refresh_token,
                                               seed_access_token):
    """
    GIVEN 1 access_token instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 access_token and update 0 access_token instance in the database and ManualException with code 404
    """
    try:
        _ = access_token_service.apply(instance=generate_uuid(), status='inactive')
    except ManualException as ex:
        assert ex.code == 400


def test_access_token_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 access_token instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 access_token and update 0 access_token instance in the database and ManualException with code 400
    """
    try:
        _ = access_token_service.apply(instance=pytest.access_token, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Misc
###########

def test_access_token_generate_token_attributes(reset_db, pause_notification, mock_kong_create_jwt_credential,
                                                seed_user):
    """
    GIVEN 0 access_token instance in the database
    WHEN the generate_token_attributes method is called
    THEN it should return a dictionary of token attributes
    """
    access_expiry = generate_expiry(app.config['ACCESS_EXP'])
    attr = access_token_service.generate_token_attributes(uuid=pytest.user.uuid, username=pytest.username,
                                                          expiry=access_expiry)
    assert 'token' in attr
    assert 'kong_jwt_id' in attr
    assert 'status' in attr
    assert 'user_uuid' in attr


def test_access_token_generate_deactivate_token_attributes(reset_db, pause_notification,
                                                           mock_kong_create_jwt_credential,
                                                           mock_kong_destroy_jwt_credential, seed_user):
    """
    GIVEN 0 access_token instance in the database
    WHEN the generate_deactivate_token_attributes method is called
    THEN it should return a dictionary of deactivated token attributes
    """
    access_expiry = generate_expiry(app.config['ACCESS_EXP'])
    attr = access_token_service.generate_token_attributes(uuid=pytest.user.uuid, username=pytest.username,
                                                          expiry=access_expiry)
    attr = access_token_service.generate_deactivate_token_attributes(username=pytest.username,
                                                                     kong_jwt_id=attr['kong_jwt_id'])
    assert 'status' in attr
    assert 'kong_jwt_id' in attr
