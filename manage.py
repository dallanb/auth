from flask import g
from flask.cli import FlaskGroup
from src import app, db
from bin import init_role, init_status
import src

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("drop_db")
def drop_db():
    db.drop_all()


@cli.command("initialize_roles")
def initialize_roles():
    with app.app_context():
        g.src = src
        init_role()
        return


@cli.command("initialize_statuses")
def initialize_statuses():
    with app.app_context():
        g.src = src
        init_status()
        return


if __name__ == "__main__":
    cli()
