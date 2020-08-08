from flask import g
import logging


def init_user_role(role_enums):
    logging.info(f"init_user_role started")
    UserRole = g.src.UserRole

    for role_enum in role_enums:
        status = UserRole(name=role_enum)
        g.src.db.session.add(status)
    g.src.db.session.commit()
    logging.info(f"init_user_role completed")
    return
