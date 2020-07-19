from flask import g
import logging


def init_user_role():
    role_enums = g.src.UserRoleEnum
    UserRole = g.src.UserRoleModel

    for role_enum in role_enums:
        role = UserRole(name=role_enum)
        g.src.db.session.add(role)
        logging.info(f"{role_enum} added")
    g.src.db.session.commit()
    return
