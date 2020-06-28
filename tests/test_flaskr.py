import os
import tempfile

import pytest

from huncho.services.auth import src


@pytest.fixture
def client():
    db_fd, src.app.config['DATABASE'] = tempfile.mkstemp()
    src.app.config['TESTING'] = True

    with src.app.test_client() as client:
        with src.app.app_context():
            src.init_db()
        yield client

    os.close(db_fd)
    os.unlink(src.app.config['DATABASE'])
