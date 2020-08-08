from flask import g
import logging


def init_user_status(status_enums):
    logging.info(f"init_user_status started")
    UserStatus = g.src.UserStatus

    for status_enum in status_enums:
        status = UserStatus(name=status_enum)
        g.src.db.session.add(status)
    g.src.db.session.commit()
    logging.info(f"init_user_status completed")
    return
