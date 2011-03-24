"""This is an interactive, phone-based adventure game."""

from __future__ import with_statement

from contextlib import closing
import os
import sqlite3

from flask import Flask, g

DATABASE = "pyteladventure.db"  # Relative to project directory
DEBUG = True
SECRET_KEY = '8djgk437fkbmnehge0ofvjgnrtoE7CVNghednxdbnvfuir'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


def get_db_path():
    path = DATABASE
    if not path.startswith("/"):
        path = os.path.join(app.root_path, os.path.pardir, DATABASE)
    return path


def get_schema_path():
    return os.path.join(app.root_path, os.path.pardir, "schema.sql")


def connect_db():
    return sqlite3.connect(get_db_path())


def init_db(create_a_few_nodes=True):
    with app.open_resource(get_schema_path()) as f:
        with closing(connect_db()) as connection:
            cursor = connection.cursor()
            cursor.executescript(f.read())
            if create_a_few_nodes:
                model = Model(cursor)
                model.create_a_few_nodes()
            connection.commit()


@app.before_request
def before_request():
    from pyteladventure.model import Model  # Import late.
    g.connection = connect_db()
    g._cursor = g.connection.cursor()
    g.model = Model(g._cursor)


@app.after_request
def after_request(response):
    g._cursor.close()
    g.connection.close()
    return response


import pyteladventure.views
from pyteladventure.model import Model