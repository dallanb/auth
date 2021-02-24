import os
import tempfile

import pytest

import src
from manage import clear_db, create_db, full_load


@pytest.fixture
def client():
    db_fd, src.app.config['DATABASE'] = tempfile.mkstemp()
    src.app.config['TESTING'] = True

    with src.app.test_client() as client:
        with src.app.app_context():
            clear_db()
            create_db()
            full_load()
        yield client

    os.close(db_fd)
    os.unlink(src.app.config['DATABASE'])
