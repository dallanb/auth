import pytest

from src import services, ManualException
from tests.helpers import generate_uuid

user_service = services.User()


###########
# Find
###########
def test_user_find(reset_db, pause_notification, seed_user):
    """
    GIVEN 1 user instance in the database
    WHEN the find method is called
    THEN it should return 1 user
    """

    users = user_service.find()
    assert users.total == 1
    assert len(users.items) == 1
    user = users.items[0]
    assert user.uuid == pytest.user.uuid


def test_user_find_by_uuid():
    """
    GIVEN 1 user instance in the database
    WHEN the find method is called with uuid
    THEN it should return 1 user
    """
    user = pytest.user
    uuid = user.uuid

    users = user_service.find(uuid=uuid)
    assert users.total == 1
    assert len(users.items) == 1
    user = users.items[0]
    assert user.uuid == uuid


def test_user_find_by_email():
    """
    GIVEN 1 user instance in the database
    WHEN the find method is called with email
    THEN it should return 1 user
    """
    user = pytest.user
    email = user.email

    users = user_service.find(email=email)
    assert users.total == 1
    assert len(users.items) == 1
    user = users.items[0]
    assert user.email == email


def test_user_find_w_pagination(pause_notification):
    """
    GIVEN 2 user instance in the database
    WHEN the find method is called with valid pagination
    THEN it should return the number of users defined in the pagination arguments
    """
    user_service.create(status='pending', role='member',
                        email='babyd@sfu.ca', password=pytest.password,
                        username='babyd')

    users_0 = user_service.find(page=1, per_page=1)
    assert users_0.total == 2
    assert len(users_0.items) == 1

    users_1 = user_service.find(page=2, per_page=1)
    assert users_1.total == 2
    assert len(users_1.items) == 1
    assert users_1.items[0] != users_0.items[0]

    users = user_service.find(page=1, per_page=2)
    assert users.total == 2
    assert len(users.items) == 2


def test_user_find_w_bad_pagination():
    """
    GIVEN 2 user instance in the database
    WHEN the find method is called with invalid pagination
    THEN it should return the 0 user
    """
    users = user_service.find(page=3, per_page=3)
    assert users.total == 2
    assert len(users.items) == 0


def test_user_find_by_email_none_found():
    """
    GIVEN 2 user instance in the database
    WHEN the find method is called with a random email
    THEN it should return the 0 user
    """
    users = user_service.find(email='junk@sfu.ca')
    assert users.total == 0
    assert len(users.items) == 0


def test_user_find_by_non_existent_column():
    """
    GIVEN 2 user instance in the database
    WHEN the find method is called with a random column
    THEN it should return the 0 user and ManualException with code 400
    """
    try:
        _ = user_service.find(junk=generate_uuid())
    except ManualException as ex:
        assert ex.code == 400


def test_user_find_by_non_existent_include():
    """
    GIVEN 2 user instance in the database
    WHEN the find method is called with a random include
    THEN it should return the 0 user and ManualException with code 400
    """
    try:
        _ = user_service.find(include=['junk'])
    except ManualException as ex:
        assert ex.code == 400


def test_user_find_by_non_existent_expand():
    """
    GIVEN 2 user instance in the database
    WHEN the find method is called with a random expand
    THEN it should return the 0 user and ManualException with code 400
    """
    try:
        _ = user_service.find(expand=['junk'])
    except ManualException as ex:
        assert ex.code == 400


###########
# Create
###########
def test_user_create(reset_db, pause_notification):
    """
    GIVEN 0 user instance in the database
    WHEN the create method is called
    THEN it should return 1 user and add 1 user instance into the database
    """
    user = user_service.create(status='pending', role='member',
                               email=pytest.email, password=pytest.password,
                               username=pytest.username)

    assert user.uuid is not None
    assert user.email == pytest.email


def test_user_create_dup(pause_notification):
    """
    GIVEN 1 user instance in the database
    WHEN the create method is called with the exact same parameters of an existing user
    THEN it should return 0 user and add 0 user instance into the database and ManualException with code 500
    """
    try:
        _ = user_service.create(status='pending', role='member',
                                email=pytest.email, password=pytest.password,
                                username=pytest.username)
    except ManualException as ex:
        assert ex.code == 500


def test_user_create_w_bad_field(pause_notification):
    """
    GIVEN 1 user instance in the database
    WHEN the create method is called with a non existent field
    THEN it should return 0 user and add 0 user instance into the database and ManualException with code 500
    """
    try:
        _ = user_service.create(status='pending', role='member',
                                email='babyd@sfu.ca', password=pytest.password,
                                username='babyd', junk='junk')
    except ManualException as ex:
        assert ex.code == 500


###########
# Update
###########
def test_user_update(reset_db, pause_notification, seed_user):
    """
    GIVEN 1 user instance in the database
    WHEN the update method is called
    THEN it should return 1 user and update 1 user instance into the database
    """
    user = user_service.update(uuid=pytest.user.uuid, password=pytest.password)
    assert user.uuid is not None

    users = user_service.find(uuid=user.uuid)
    assert users.total == 1
    assert len(users.items) == 1


def test_user_update_w_bad_uuid(reset_db, pause_notification, seed_user):
    """
    GIVEN 1 user instance in the database
    WHEN the update method is called with random uuid
    THEN it should return 0 user and update 0 user instance into the database and ManualException with code 404
    """
    try:
        _ = user_service.update(uuid=generate_uuid(), password=pytest.password)
    except ManualException as ex:
        assert ex.code == 404


def test_user_update_w_bad_field(pause_notification):
    """
    GIVEN 1 user instance in the database
    WHEN the update method is called with bad field
    THEN it should return 0 user and update 0 user instance in the database and ManualException with code 400
    """
    try:
        _ = user_service.update(uuid=pytest.user.uuid, junk='junk')
    except ManualException as ex:
        assert ex.code == 400


###########
# Apply
###########
def test_user_apply(reset_db, pause_notification, seed_user):
    """
    GIVEN 1 user instance in the database
    WHEN the apply method is called
    THEN it should return 1 user and update 1 user instance in the database
    """
    user = user_service.apply(instance=pytest.user, password=pytest.password)
    assert user.uuid is not None

    users = user_service.find(uuid=user.uuid)
    assert users.total == 1
    assert len(users.items) == 1


def test_user_apply_w_bad_user(reset_db, pause_notification, seed_user):
    """
    GIVEN 1 user instance in the database
    WHEN the apply method is called with random uuid
    THEN it should return 0 user and update 0 user instance in the database and ManualException with code 404
    """
    try:
        _ = user_service.apply(instance=generate_uuid(), password=pytest.password)
    except ManualException as ex:
        assert ex.code == 400


def test_user_apply_w_bad_field(pause_notification):
    """
    GIVEN 1 user instance in the database
    WHEN the apply method is called with bad field
    THEN it should return 0 user and update 0 user instance in the database and ManualException with code 400
    """
    try:
        _ = user_service.apply(instance=pytest.user, junk='junk')
    except ManualException as ex:
        assert ex.code == 400
