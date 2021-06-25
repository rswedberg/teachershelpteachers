# http://flask.pocoo.org/docs/1.0/tutorial/database/
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db_login():
    if "db" not in g:
        g.db = sqlite3.connect(
            "sqlite_db", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def get_db_questions():
    if "db" not in g:
        g.db = sqlite3.connect(
            "questions_db", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db 

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db_login():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

def init_db_questions():
    db = get_db()

    with current_app.open_resource("questions.sql") as f:
        db.executescript(f.read().decode("utf8"))
    click.echo("Initialized the database.")

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db_login()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
