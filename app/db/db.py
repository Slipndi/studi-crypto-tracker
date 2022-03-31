import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext

def get_db_connection() : 
    connection = sqlite3.connect('app.sql')
    connection.row_factory=sqlite3.Row
    return connection

    

    