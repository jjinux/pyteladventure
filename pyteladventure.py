"""This is an interactive, phone-based adventure game."""

from __future__ import with_statement

from contextlib import closing
import os
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash

DATABASE = "pyteladventure.db"  # Relative to project directory
DEBUG = False
SECRET_KEY = '8djgk437fkbmnehge0ofvjgnrtoE7CVNghednxdbnvfuir'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


def get_db_path():
    path = DATABASE
    if not path.startswith("/"):
        path = os.path.join(app.root_path, DATABASE)
    return path


def connect_db():
    return sqlite3.connect(get_db_path())


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=()):
    """Query the database and return a list of dicts.

    For instance:

        query_db('select * from users where username = ?', [username])

    """
    cur = g.db.execute(query, args)
    rv = {}
    for row in cur.fetchall():
        item = {}
        for idx, value in enumerate(row):
            key = cur.description[idx][0]
            item[key] = value
        rv.append(item)
    return rv


def query_db_for_one_record(query, args=()):
    """Call query_db and return exactly one record as a dict.

    If there isn't exactly one record, raise an IndexError.

    """
    rv = query_db(query, args)
    if len(rv) != 1:
        raise IndexError("Expected exactly one row; %s rows returned" %
                         len(rv))
    return rv[0]


@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response


if __name__ == '__main__':
    app.run()

# XXX
# Setup README like Flaskr.
# Setup README like Teladventure.