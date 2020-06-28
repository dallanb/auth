from flask import g
import logging


def init_role():
    role_enums = g.src.RoleEnum
    Role = g.src.Role

    for role_enum in role_enums:
        role = Role(name=role_enum)
        g.src.db.session.add(role)
        logging.info(f"{role_enum} added")
    g.src.db.session.commit()
    return
