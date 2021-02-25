from src import db, TokenStatus


def init_token_status(status_enums):
    for status_enum in status_enums:
        status = TokenStatus(name=status_enum)
        db.session.add(status)
    db.session.commit()
    return
