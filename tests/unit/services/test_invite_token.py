import pytest

from src import services, ManualException, app
from src.common import generate_expiry
from tests.helpers import generate_uuid

invite_token_service = services.InviteToken()


###########
# Find
###########
def test_invite_token_find(reset_db, pause_notification, seed_invite_token):
    """
    GIVEN 1 invite_token instance in the database
    WHEN the find method is called
    THEN it should return 1 invite_token
    """

    invite_tokens = invite_token_service.find()
    assert invite_tokens.total == 1
    assert len(invite_tokens.items) == 1
    invite_token = invite_tokens.items[0]
    assert invite_token.uuid == pytest.invite_token.uuid


def test_invite_token_find_by_uuid():
    """
    GIVEN 1 invite_token instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 invite_token
    """
    invite_token = pytest.invite_token
    uuid = invite_token.uuid

    invite_tokens = invite_token_service.find(uuid=uuid)
    assert invite_tokens.total == 1
    assert len(invite_tokens.items) == 1
    invite_token = invite_tokens.items[0]
    assert invite_token.uuid == uuid


def test_invite_token_find_by_token():
    """
    GIVEN 1 invite_token instance in the database
    WHEN the find method is called with token
    THEN it should return 1 invite_token
    """
    invite_token = pytest.invite_token
    token = invite_token.token

    invite_tokens = invite_token_service.find(token=token)
    assert invite_tokens.total == 1
    assert len(invite_tokens.items) == 1
    invite_token = invite_tokens.items[0]
    assert invite_token.token == token


def test_invite_token_find_w_pagination(pause_notification, seed_invite_token):
    """
    GIVEN 2 invite_token instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of invite_tokens defined in the pagination arguments
    """
    invite_tokens_0 = invite_token_service.find(page=1, per_page=1)
    assert invite_tokens_0.total == 2
    assert len(invite_tokens_0.items) == 1

    invite_tokens_1 = invite_token_service.find(page=2, per_page=1)
    assert invite_tokens_1.total == 2
    assert len(invite_tokens_1.items) == 1
    assert invite_tokens_1.items[0] != invite_tokens_0.items[0]

    invite_tokens = invite_token_service.find(page=1, per_page=2)
    assert invite_tokens.total == 2
    assert len(invite_tokens.items) == 2


def test_invite_token_find_w_bad_pagination():
    """
    GIVEN 2 invite_token instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 invite_token
    """
    invite_tokens = invite_token_service.find(page=3, per_page=3)
    assert invite_tokens.total == 2
    assert len(invite_tokens.items) == 0


def test_invite_token_find_by_token_none_found():
    """
    GIVEN 2 invite_token instance in the database
    WHEN the find method is called with a random token
    THEN it should return the 0 invite_token
    """
    invite_tokens = invite_token_service.find(token='123456')
    assert invite_tokens.total == 0
    assert len(invite_tokens.items) == 0


def test_invite_token_find_by_non_existent_column():
    """
    GIVEN 2 invite_token instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 invite_token and ManualException with code 400
    """
    try:
        _ = invite_token_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_invite_token_find_by_non_existent_include():
    """
    GIVEN 2 invite_token instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 invite_token and ManualException with code 400
    """
    try:
        _ = invite_token_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_invite_token_find_by_non_existent_expand():
    """
    GIVEN 2 invite_token instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 invite_token and ManualException with code 400
    """
    try:
        _ = invite_token_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_invite_token_create(reset_db, pause_notification):
    """
    GIVEN 0 invite_token instance in the database
    WHEN the create method is called
    THEN it should return 1 invite_token and add 1 invite_token instance into the database
    """
    invite_token = invite_token_service.create(email=pytest.email, status='active')

    assert invite_token.uuid is not None
    assert invite_token.token is not None


def test_invite_token_create_dup(pause_notification):
    """
    GIVEN 1 invite_token instance in the database
    WHEN the create method is called with the exact same parameters of an existing invite_token
    THEN it should return 1 invite_token and add 1 invite_token instance into the database
    """
    invite_token = invite_token_service.create(email=pytest.email, status='active')
    assert invite_token is not None


def test_invite_token_create_w_bad_field(pause_notification):
    """
    GIVEN 1 invite_token instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 invite_token and add 0 invite_token instance into the database and ManualException with code 500
    """
    try:
        _ = invite_token_service.create(email=pytest.email, status='active', junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_invite_token_update(reset_db, pause_notification, seed_invite_token):
    """
    GIVEN 1 invite_token instance in the database
    WHEN the update method is called
    THEN it should return 1 invite_token and update 1 invite_token instance into the database
    """
    invite_token = invite_token_service.update(uuid=pytest.invite_token.uuid, status='inactive')
    assert invite_token.uuid is not None

    invite_tokens = invite_token_service.find(uuid=invite_token.uuid)
    assert invite_tokens.total == 1
    assert len(invite_tokens.items) == 1


def test_invite_token_update_w_bad_uuid(reset_db, pause_notification, seed_invite_token):
    """
    GIVEN 1 invite_token instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 invite_token and update 0 invite_token instance into the database and ManualException with code 404
    """
    try:
        _ = invite_token_service.update(uuid=generate_uuid(), status='inactive')
    except ManualException as ex:
        assert ex.code == 404


def test_invite_token_update_w_bad_field(reset_db, pause_notification, seed_invite_token):
    """
    GIVEN 1 invite_token instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 invite_token and update 0 invite_token instance in the database and ManualException with code 400
    """
    try:
        _ = invite_token_service.update(uuid=pytest.invite_token.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_invite_token_apply(reset_db, pause_notification, seed_invite_token):
    """
    GIVEN 1 invite_token instance in the database
    WHEN the apply method is called
    THEN it should return 1 invite_token and update 1 invite_token instance in the database
    """
    invite_token = invite_token_service.apply(instance=pytest.invite_token, status='inactive')
    assert invite_token.uuid is not None

    invite_tokens = invite_token_service.find(uuid=invite_token.uuid)
    assert invite_tokens.total == 1
    assert len(invite_tokens.items) == 1


def test_invite_token_apply_w_bad_invite_token(reset_db, pause_notification, seed_invite_token):
    """
    GIVEN 1 invite_token instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 invite_token and update 0 invite_token instance in the database and ManualException with code 404
    """
    try:
        _ = invite_token_service.apply(instance=generate_uuid(), status='inactive')
    except ManualException as ex:
        assert ex.code == 400


def test_invite_token_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 invite_token instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 invite_token and update 0 invite_token instance in the database and ManualException with code 400
    """
    try:
        _ = invite_token_service.apply(instance=pytest.invite_token, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Misc
###########
def test_invite_token_confirm_token(reset_db, pause_notification, seed_invite_token):
    """
    GIVEN 1 invite_token instance in the database
    WHEN the confirm_token method is called
    THEN it should return True if a token exists
    """
    assert invite_token_service.confirm_token(token=pytest.invite_token.token, email=pytest.invite_token.email)


def test_invite_token_deactivate_token(pause_notification, seed_invite_token):
    """
    GIVEN 2 invite_token instance in the database
    WHEN the deactivate_tokens method is called
    THEN it should return nothing but set all active tokens to inactive
    """
    active_tokens = invite_token_service.find(email=pytest.email, status='active')
    assert active_tokens.total == 2

    invite_token_service.deactivate_tokens(email=pytest.email)
    inactive_tokens = invite_token_service.find(email=pytest.email, status='inactive')
    assert inactive_tokens.total == 2
