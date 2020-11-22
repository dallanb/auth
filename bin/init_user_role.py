import logging

from src import db, UserRole


def init_user_role(role_enums):
    logging.info(f"init_user_role started")

    for role_enum in role_enums:
        status = UserRole(name=role_enum)
        db.session.add(status)
    db.session.commit()
    logging.info(f"init_user_role completed")
    return
