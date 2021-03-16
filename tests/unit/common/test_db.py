import pytest

from src.common import DB, Cleaner
from src.models import *
from tests.helpers import generate_uuid

db = DB()
cleaner = Cleaner()


def test_init(reset_db, pause_notification):
    """
    GIVEN a db instance
    WHEN calling the init method of the db instance on the InviteToken model
    THEN it should return the invite_token instance
    """
    instance = db.init(model=InviteToken, email=pytest.email, status='active')
    assert cleaner.is_mapped(instance) == instance
    assert cleaner.is_uuid(instance.uuid) is not None
    assert instance.email == pytest.email

    db.rollback()


def test_count(pause_notification):
    """
    GIVEN a db instance
    WHEN calling the count method of the db instance on the InviteToken model
    THEN it should return the number of invite_token instances
    """
    count = db.count(model=InviteToken)
    assert count == 0

    invite_token = db.init(model=InviteToken, email=pytest.email, status='active')
    _ = db.save(instance=invite_token)
    count = db.count(model=InviteToken)
    assert count == 1


def test_add(reset_db, pause_notification):
    """
    GIVEN a db instance
    WHEN calling the add method of the db instance on a invite_token instance
    THEN it should add a invite_token instance to the database
    """
    instance = db.init(model=InviteToken, email=pytest.email, status='active')
    invite_token = db.add(instance=instance)
    assert cleaner.is_uuid(invite_token.uuid) is not None
    assert invite_token.email == pytest.email

    db.rollback()
    assert db.count(model=InviteToken) == 0


def test_commit(reset_db, pause_notification):
    """
    GIVEN a db instance
    WHEN calling the commit method of the db instance on a invite_token instance
    THEN it should add a invite_token instance to the database
    """
    instance = db.init(model=InviteToken, email=pytest.email, status='active')
    invite_token = db.add(instance=instance)
    assert cleaner.is_uuid(invite_token.uuid) is not None
    assert invite_token.email == pytest.email

    db.rollback()
    assert db.count(model=InviteToken) == 0

    _ = db.add(instance=instance)
    db.commit()
    assert db.count(model=InviteToken) == 1

    instance_0 = db.init(model=InviteToken, email=pytest.email, status='active')
    instance_1 = db.init(model=InviteToken, email=pytest.email, status='active')
    instance_2 = db.init(model=InviteToken, email=pytest.email, status='active')
    db.add(instance=instance_0)
    db.add(instance=instance_1)
    db.add(instance=instance_2)
    db.commit()
    assert db.count(model=InviteToken) == 4


def test_save(reset_db, pause_notification):
    """
    GIVEN a db instance
    WHEN calling the save method of the db instance on a invite_token instance
    THEN it should add a invite_token instance to the database
    """
    instance = db.init(model=InviteToken, email=pytest.email, status='active')
    assert cleaner.is_uuid(instance.uuid) is not None
    assert instance.email == pytest.email
    invite_token = db.save(instance=instance)
    assert db.count(model=InviteToken) == 1
    assert invite_token.email == pytest.email


def test_find():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance
    THEN it should find a invite_token instance from the database
    """
    result = db.find(model=InviteToken)
    assert result.total == 1
    assert len(result.items) == 1

    result = db.find(model=InviteToken, uuid=generate_uuid())
    assert result.total == 0


def test_destroy(pause_notification):
    """
    GIVEN a db instance
    WHEN calling the destroy method of the db instance on a invite_token instance
    THEN it should remove the invite_token instance from the database
    """
    result = db.find(model=InviteToken)
    assert result.total == 1
    assert len(result.items) == 1
    instance = result.items[0]

    assert db.destroy(instance=instance)
    assert db.count(model=InviteToken) == 0


def test_rollback(reset_db, pause_notification):
    """
    GIVEN a db instance
    WHEN calling the rollback method of the db instance
    THEN it should rollback a invite_token instance from being inserted the database
    """
    instance = db.init(model=InviteToken, email=pytest.email, status='active')
    db.rollback()
    db.commit()
    assert db.count(model=InviteToken) == 0

    instance = db.init(model=InviteToken, email=pytest.email, status='active')
    db.save(instance=instance)
    db.rollback()
    assert db.count(model=InviteToken) == 1


def test_clean_query(reset_db):
    """
    GIVEN a db instance
    WHEN calling the clean_query method of the db instance
    THEN it should return a query
    """
    query = db.clean_query(model=InviteToken)
    assert query is not None


def test_run_query(reset_db, pause_notification, seed_invite_token):
    """
    GIVEN a db instance
    WHEN calling the run_query method of the db instance with a valid query
    THEN it should return the query result
    """
    query = db.clean_query(model=InviteToken)
    invite_token = db.run_query(query=query)
    assert invite_token.total == 1


def test_equal_filter():
    """
    GIVEN a db instance
    WHEN calling the find method of the db instance with an equal filter
    THEN it should return the query result
    """
    email = pytest.email
    invite_token = db.find(model=InviteToken, email=email)
    assert invite_token.total == 1

    invite_token = db.find(model=InviteToken, email=email, uuid=pytest.invite_token.uuid)
    assert invite_token.items[0] == pytest.invite_token

# def test_has_key_filter():
#     """
#     GIVEN a db instance
#     WHEN calling the find method of the db instance with a has_key filter
#     THEN it should return the query result
#     """
#     
#
#     invite_token = db.find(model=InviteToken)
#     assert invite_token.total == 2
#
#     invite_token = db.find(model=InviteToken, has_key={'uuid': global_invite_token.uuid})
#     assert invite_token.total == 0
