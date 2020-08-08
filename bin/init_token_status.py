from flask import g
import logging


def init_token_status(status_enums):
    logging.info(f"init_token_status started")
    TokenStatus = g.src.TokenStatus

    for status_enum in status_enums:
        status = TokenStatus(name=status_enum)
        g.src.db.session.add(status)
    g.src.db.session.commit()
    logging.info(f"init_token_status completed")
    return
