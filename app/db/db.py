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
    
def delete_crypto(cryptomonnaie_id) :
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM crypto_value WHERE crypto_id = ?', (cryptomonnaie_id,))
    connection.commit()

def update_crypto(cryptomonnaie_id, cryptomonnaie_quantity):
    connection = get_connection()
    cursor=connection.cursor()
    cursor.execute('SELECT id, crypto_id,quantity FROM crypto_value WHERE crypto_id = ? ORDER BY Quantity, price ', (cryptomonnaie_id,))
    query_result = cursor.fetchall()
        
    # si il existe qu'une ligne dans la base de donnée, on la met à jour
    if len(query_result) == 1 :
        new_quantity = query_result[0]['quantity'] - cryptomonnaie_quantity
        cursor.execute('UPDATE crypto_value SET quantity = ? WHERE crypto_id = ? ', (new_quantity, cryptomonnaie_id ))
        connection.commit()
    else : 
    # Sinon on vérifie ligne par ligne et fait évoluer la quantité
        new_quantity = cryptomonnaie_quantity
        for id, crypto_id, quantity in query_result : 
            # tant que la nouvelle quantité est supérieur à 0
                if quantity <= new_quantity :
                    new_quantity -= quantity
                    cursor.execute('DELETE FROM crypto_value where id = ?', (id, ))
                else : 
                    new_quantity = quantity-new_quantity
                    cursor.execute('UPDATE crypto_value SET quantity = ? WHERE crypto_id = ? ', (new_quantity, cryptomonnaie_id ))
                    new_quantity=0
        connection.commit()
        flash("Mise à jour réussie", "success")
    connection.close()
    
def insert_amount_in_database(amount):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO evolution_gain (value, date) VALUES (?, ?)",
                    (amount, date.today())
                )
    connection.commit()
    connection.close()