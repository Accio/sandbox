"""Connect to database"""
import sqlite3

import click
# g is a special object that is unique for each request to store data
# current_app is another special object that points to the Flask applicaiton handling the request
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    db = get_db();

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# define a command-line command 'init-db' that calls the init_db function. CLI=Command-line interface
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    # tell Flask to call close_db when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    # add a new command that can be called with the flask command
    app.cli.add_command(init_db_command)

