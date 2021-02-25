import pytest

from src import services, ManualException, app
from src.common import generate_expiry
from tests.helpers import generate_uuid

reset_password_token_service = services.ResetPasswordToken()


###########
# Find
###########
def test_reset_password_token_find(reset_db, pause_notification, seed_reset_password_token):
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the find method is called
    THEN it should return 1 reset_password_token
    """

    reset_password_tokens = reset_password_token_service.find()
    assert reset_password_tokens.total == 1
    assert len(reset_password_tokens.items) == 1
    reset_password_token = reset_password_tokens.items[0]
    assert reset_password_token.uuid == pytest.reset_password_token.uuid


def test_reset_password_token_find_by_uuid():
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 reset_password_token
    """
    reset_password_token = pytest.reset_password_token
    uuid = reset_password_token.uuid

    reset_password_tokens = reset_password_token_service.find(uuid=uuid)
    assert reset_password_tokens.total == 1
    assert len(reset_password_tokens.items) == 1
    reset_password_token = reset_password_tokens.items[0]
    assert reset_password_token.uuid == uuid


def test_reset_password_token_find_by_token():
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the find method is called with token
    THEN it should return 1 reset_password_token
    """
    reset_password_token = pytest.reset_password_token
    token = reset_password_token.token

    reset_password_tokens = reset_password_token_service.find(token=token)
    assert reset_password_tokens.total == 1
    assert len(reset_password_tokens.items) == 1
    reset_password_token = reset_password_tokens.items[0]
    assert reset_password_token.token == token


def test_reset_password_token_find_w_pagination(pause_notification, seed_reset_password_token):
    """
    GIVEN 2 reset_password_token instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of reset_password_tokens defined in the pagination arguments
    """
    reset_password_tokens_0 = reset_password_token_service.find(page=1, per_page=1)
    assert reset_password_tokens_0.total == 2
    assert len(reset_password_tokens_0.items) == 1

    reset_password_tokens_1 = reset_password_token_service.find(page=2, per_page=1)
    assert reset_password_tokens_1.total == 2
    assert len(reset_password_tokens_1.items) == 1
    assert reset_password_tokens_1.items[0] != reset_password_tokens_0.items[0]

    reset_password_tokens = reset_password_token_service.find(page=1, per_page=2)
    assert reset_password_tokens.total == 2
    assert len(reset_password_tokens.items) == 2


def test_reset_password_token_find_w_bad_pagination():
    """
    GIVEN 2 reset_password_token instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 reset_password_token
    """
    reset_password_tokens = reset_password_token_service.find(page=3, per_page=3)
    assert reset_password_tokens.total == 2
    assert len(reset_password_tokens.items) == 0


def test_reset_password_token_find_by_token_none_found():
    """
    GIVEN 2 reset_password_token instance in the database
    WHEN the find method is called with a random token
    THEN it should return the 0 reset_password_token
    """
    reset_password_tokens = reset_password_token_service.find(token='123456')
    assert reset_password_tokens.total == 0
    assert len(reset_password_tokens.items) == 0


def test_reset_password_token_find_by_non_existent_column():
    """
    GIVEN 2 reset_password_token instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 reset_password_token and ManualException with code 400
    """
    try:
        _ = reset_password_token_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_reset_password_token_find_by_non_existent_include():
    """
    GIVEN 2 reset_password_token instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 reset_password_token and ManualException with code 400
    """
    try:
        _ = reset_password_token_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_reset_password_token_find_by_non_existent_expand():
    """
    GIVEN 2 reset_password_token instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 reset_password_token and ManualException with code 400
    """
    try:
        _ = reset_password_token_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_reset_password_token_create(reset_db, pause_notification):
    """
    GIVEN 0 reset_password_token instance in the database
    WHEN the create method is called
    THEN it should return 1 reset_password_token and add 1 reset_password_token instance into the database
    """
    reset_password_token = reset_password_token_service.create(email=pytest.email, status='active')

    assert reset_password_token.uuid is not None
    assert reset_password_token.token is not None


def test_reset_password_token_create_dup(pause_notification):
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the create method is called with the exact same parameters of an existing reset_password_token
    THEN it should return 1 reset_password_token and add 1 reset_password_token instance into the database
    """
    reset_password_token = reset_password_token_service.create(email=pytest.email, status='active')
    assert reset_password_token is not None


def test_reset_password_token_create_w_bad_field(pause_notification):
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 reset_password_token and add 0 reset_password_token instance into the database and ManualException with code 500
    """
    try:
        _ = reset_password_token_service.create(email=pytest.email, status='active', junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_reset_password_token_update(reset_db, pause_notification, seed_reset_password_token):
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the update method is called
    THEN it should return 1 reset_password_token and update 1 reset_password_token instance into the database
    """
    reset_password_token = reset_password_token_service.update(uuid=pytest.reset_password_token.uuid, status='inactive')
    assert reset_password_token.uuid is not None

    reset_password_tokens = reset_password_token_service.find(uuid=reset_password_token.uuid)
    assert reset_password_tokens.total == 1
    assert len(reset_password_tokens.items) == 1


def test_reset_password_token_update_w_bad_uuid(reset_db, pause_notification, seed_reset_password_token):
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 reset_password_token and update 0 reset_password_token instance into the database and ManualException with code 404
    """
    try:
        _ = reset_password_token_service.update(uuid=generate_uuid(), status='inactive')
    except ManualException as ex:
        assert ex.code == 404


def test_reset_password_token_update_w_bad_field(reset_db, pause_notification, seed_reset_password_token):
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 reset_password_token and update 0 reset_password_token instance in the database and ManualException with code 400
    """
    try:
        _ = reset_password_token_service.update(uuid=pytest.reset_password_token.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_reset_password_token_apply(reset_db, pause_notification, seed_reset_password_token):
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the apply method is called
    THEN it should return 1 reset_password_token and update 1 reset_password_token instance in the database
    """
    reset_password_token = reset_password_token_service.apply(instance=pytest.reset_password_token, status='inactive')
    assert reset_password_token.uuid is not None

    reset_password_tokens = reset_password_token_service.find(uuid=reset_password_token.uuid)
    assert reset_password_tokens.total == 1
    assert len(reset_password_tokens.items) == 1


def test_reset_password_token_apply_w_bad_reset_password_token(reset_db, pause_notification, seed_reset_password_token):
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 reset_password_token and update 0 reset_password_token instance in the database and ManualException with code 404
    """
    try:
        _ = reset_password_token_service.apply(instance=generate_uuid(), status='inactive')
    except ManualException as ex:
        assert ex.code == 400


def test_reset_password_token_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 reset_password_token instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 reset_password_token and update 0 reset_password_token instance in the database and ManualException with code 400
    """
    try:
        _ = reset_password_token_service.apply(instance=pytest.reset_password_token, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Misc
###########
def test_reset_password_token_deactivate_token(pause_notification, seed_reset_password_token):
    """
    GIVEN 2 reset_password_token instance in the database
    WHEN the deactivate_tokens method is called
    THEN it should return nothing but set all active tokens to inactive
    """
    active_tokens = reset_password_token_service.find(email=pytest.email, status='active')
    assert active_tokens.total == 2

    reset_password_token_service.deactivate_tokens(email=pytest.email)
    inactive_tokens = reset_password_token_service.find(email=pytest.email, status='inactive')
    assert inactive_tokens.total == 2
