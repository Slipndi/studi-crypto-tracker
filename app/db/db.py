import sqlite3
from datetime import date
from flask import flash

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

def insert_new_crypto_quantity(cryptomonnaie_id, cryptomonnaie_quantity, cryptomonnaie_name, cryptomonnaie_unique_price) :
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO crypto_value (crypto_id, name, price, quantity, date) VALUES (?, ?, ?, ?, ?)",(cryptomonnaie_id, cryptomonnaie_name,cryptomonnaie_unique_price, cryptomonnaie_quantity, date.today()))
    connection.commit()
    flash("Transaction Validée", "success")
    connection.close()