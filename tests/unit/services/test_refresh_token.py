import pytest

from src import services, ManualException, app
from src.common import generate_expiry
from tests.helpers import generate_uuid

refresh_token_service = services.RefreshToken()


###########
# Find
###########
def test_refresh_token_find(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                            seed_refresh_token):
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the find method is called
    THEN it should return 1 refresh_token
    """

    refresh_tokens = refresh_token_service.find()
    assert refresh_tokens.total == 1
    assert len(refresh_tokens.items) == 1
    refresh_token = refresh_tokens.items[0]
    assert refresh_token.uuid == pytest.refresh_token.uuid


def test_refresh_token_find_by_uuid():
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 refresh_token
    """
    refresh_token = pytest.refresh_token
    uuid = refresh_token.uuid

    refresh_tokens = refresh_token_service.find(uuid=uuid)
    assert refresh_tokens.total == 1
    assert len(refresh_tokens.items) == 1
    refresh_token = refresh_tokens.items[0]
    assert refresh_token.uuid == uuid


def test_refresh_token_find_by_token():
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the find method is called with token
    THEN it should return 1 refresh_token
    """
    refresh_token = pytest.refresh_token
    token = refresh_token.token

    refresh_tokens = refresh_token_service.find(token=token)
    assert refresh_tokens.total == 1
    assert len(refresh_tokens.items) == 1
    refresh_token = refresh_tokens.items[0]
    assert refresh_token.token == token


def test_refresh_token_find_w_pagination(pause_notification, seed_refresh_token):
    """
    GIVEN 2 refresh_token instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of refresh_tokens defined in the pagination arguments
    """
    refresh_tokens_0 = refresh_token_service.find(page=1, per_page=1)
    assert refresh_tokens_0.total == 2
    assert len(refresh_tokens_0.items) == 1

    refresh_tokens_1 = refresh_token_service.find(page=2, per_page=1)
    assert refresh_tokens_1.total == 2
    assert len(refresh_tokens_1.items) == 1
    assert refresh_tokens_1.items[0] != refresh_tokens_0.items[0]

    refresh_tokens = refresh_token_service.find(page=1, per_page=2)
    assert refresh_tokens.total == 2
    assert len(refresh_tokens.items) == 2


def test_refresh_token_find_w_bad_pagination():
    """
    GIVEN 2 refresh_token instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 refresh_token
    """
    refresh_tokens = refresh_token_service.find(page=3, per_page=3)
    assert refresh_tokens.total == 2
    assert len(refresh_tokens.items) == 0


def test_refresh_token_find_by_token_none_found():
    """
    GIVEN 2 refresh_token instance in the database
    WHEN the find method is called with a random token
    THEN it should return the 0 refresh_token
    """
    refresh_tokens = refresh_token_service.find(token='123456')
    assert refresh_tokens.total == 0
    assert len(refresh_tokens.items) == 0


def test_refresh_token_find_by_non_existent_column():
    """
    GIVEN 2 refresh_token instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 refresh_token and ManualException with code 400
    """
    try:
        _ = refresh_token_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_refresh_token_find_by_non_existent_include():
    """
    GIVEN 2 refresh_token instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 refresh_token and ManualException with code 400
    """
    try:
        _ = refresh_token_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_refresh_token_find_by_non_existent_expand():
    """
    GIVEN 2 refresh_token instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 refresh_token and ManualException with code 400
    """
    try:
        _ = refresh_token_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_refresh_token_create(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user):
    """
    GIVEN 0 refresh_token instance in the database
    WHEN the create method is called
    THEN it should return 1 refresh_token and add 1 refresh_token instance into the database
    """
    access_expiry = generate_expiry(app.config['REFRESH_EXP'])
    attr = refresh_token_service.generate_token_attributes(uuid=pytest.user.uuid, username=pytest.user.username,
                                                           expiry=access_expiry)
    refresh_token = refresh_token_service.create(**attr)

    assert refresh_token.uuid is not None
    assert refresh_token.token is not None


def test_refresh_token_create_dup(pause_notification, mock_kong_create_jwt_credential):
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the create method is called with the exact same parameters of an existing refresh_token
    THEN it should return 1 refresh_token and add 1 refresh_token instance into the database
    """
    access_expiry = generate_expiry(app.config['REFRESH_EXP'])
    attr = refresh_token_service.generate_token_attributes(uuid=pytest.user.uuid, username=pytest.user.username,
                                                           expiry=access_expiry)
    refresh_token = refresh_token_service.create(**attr)
    assert refresh_token is not None


def test_refresh_token_create_w_bad_field(pause_notification, mock_kong_create_jwt_credential):
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 refresh_token and add 0 refresh_token instance into the database and ManualException with code 500
    """
    try:
        access_expiry = generate_expiry(app.config['REFRESH_EXP'])
        attr = refresh_token_service.generate_token_attributes(uuid=pytest.user.uuid, username=pytest.user.username,
                                                               expiry=access_expiry)
        _ = refresh_token_service.create(**attr, refresh_token=pytest.refresh_token, junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_refresh_token_update(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                              seed_refresh_token):
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the update method is called
    THEN it should return 1 refresh_token and update 1 refresh_token instance into the database
    """
    refresh_token = refresh_token_service.update(uuid=pytest.refresh_token.uuid, status='inactive')
    assert refresh_token.uuid is not None

    refresh_tokens = refresh_token_service.find(uuid=refresh_token.uuid)
    assert refresh_tokens.total == 1
    assert len(refresh_tokens.items) == 1


def test_refresh_token_update_w_bad_uuid(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                                         seed_refresh_token):
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 refresh_token and update 0 refresh_token instance into the database and ManualException with code 404
    """
    try:
        _ = refresh_token_service.update(uuid=generate_uuid(), status='inactive')
    except ManualException as ex:
        assert ex.code == 404


def test_refresh_token_update_w_bad_field(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                                          seed_refresh_token):
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 refresh_token and update 0 refresh_token instance in the database and ManualException with code 400
    """
    try:
        _ = refresh_token_service.update(uuid=pytest.refresh_token.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_refresh_token_apply(reset_db, pause_notification, mock_kong_create_jwt_credential, seed_user,
                             seed_refresh_token):
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the apply method is called
    THEN it should return 1 refresh_token and update 1 refresh_token instance in the database
    """
    refresh_token = refresh_token_service.apply(instance=pytest.refresh_token, status='inactive')
    assert refresh_token.uuid is not None

    refresh_tokens = refresh_token_service.find(uuid=refresh_token.uuid)
    assert refresh_tokens.total == 1
    assert len(refresh_tokens.items) == 1


def test_refresh_token_apply_w_bad_refresh_token(reset_db, pause_notification, mock_kong_create_jwt_credential,
                                                 seed_user,
                                                 seed_refresh_token):
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 refresh_token and update 0 refresh_token instance in the database and ManualException with code 404
    """
    try:
        _ = refresh_token_service.apply(instance=generate_uuid(), status='inactive')
    except ManualException as ex:
        assert ex.code == 400


def test_refresh_token_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 refresh_token instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 refresh_token and update 0 refresh_token instance in the database and ManualException with code 400
    """
    try:
        _ = refresh_token_service.apply(instance=pytest.refresh_token, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Misc
###########

def test_refresh_token_generate_token_attributes(reset_db, pause_notification, mock_kong_create_jwt_credential,
                                                 seed_user):
    """
    GIVEN 0 refresh_token instance in the database
    WHEN the generate_token_attributes method is called
    THEN it should return a dictionary of token attributes
    """
    access_expiry = generate_expiry(app.config['REFRESH_EXP'])
    attr = refresh_token_service.generate_token_attributes(uuid=pytest.user.uuid, username=pytest.username,
                                                           expiry=access_expiry)
    assert 'token' in attr
    assert 'status' in attr
    assert 'user_uuid' in attr
