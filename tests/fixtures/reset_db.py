import pytest

from bin import init_user_status, init_user_role, init_token_status
from src import db, common


@pytest.fixture(scope='function')
def reset_db():
    # delete
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    # create
    db.create_all()
    db.session.commit()
    # load
    init_user_status(status_enums=common.UserStatusEnum)
    init_user_role(role_enums=common.UserRoleEnum)
    init_token_status(status_enums=common.TokenStatusEnum)
