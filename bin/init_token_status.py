import logging

from src import db, TokenStatus


def init_token_status(status_enums):
    logging.info(f"init_token_status started")

    for status_enum in status_enums:
        status = TokenStatus(name=status_enum)
        db.session.add(status)
    db.session.commit()
    logging.info(f"init_token_status completed")
    return
