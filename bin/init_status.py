from flask import g
import logging


def init_status():
    status_enums = g.src.StatusEnum
    Status = g.src.Status

    for status_enum in status_enums:
        status = Status(name=status_enum)
        g.src.db.session.add(status)
        logging.info(f"{status_enum} added")
    g.src.db.session.commit()
    return
