from multiprocessing import connection
import sqlite3
import click

from flask import flash
from flask.cli import with_appcontext

def get_connection() :
    connection = sqlite3.connect('app.sqlite')
    connection.row_factory=sqlite3.Row
    return connection

def get_crypto_in_database() :
    connection=get_connection()
    cursor = connection.cursor()
    # récupération des id et prix dans la base de donnée
    cursor.execute("SELECT crypto_id, max(price) price, sum(quantity) quantity FROM crypto_value group by crypto_id order by crypto_id")
    data_from_local_database = cursor.fetchall()
    connection.close()
    return data_from_local_database