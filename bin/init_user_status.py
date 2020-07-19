from flask import g
import logging


def init_user_status():
    status_enums = g.src.UserStatusEnum
    UserStatus = g.src.UserStatusModel

    for status_enum in status_enums:
        status = UserStatus(name=status_enum)
        g.src.db.session.add(status)
        logging.info(f"{status_enum} added")
    g.src.db.session.commit()
    return
