import logging

from src import db, UserStatus


def init_user_status(status_enums):
    logging.info(f"init_user_status started")

    for status_enum in status_enums:
        status = UserStatus(name=status_enum)
        db.session.add(status)
    db.session.commit()
    logging.info(f"init_user_status completed")
    return
