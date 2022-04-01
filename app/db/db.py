import sqlite3
import os
from flaskext.mysql import MySQL
from datetime import date
from flask import flash




def get_connection() :
    mysql = MySQL(
    host=os.getenv("DB_HOST"), 
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_DATABASE")
    )
    return mysql.get_db()

def get_crypto_in_database() -> list :
    """Récupération de toutes les cryptomonnaies insérées dans la table crypto_value
    groupées par leurs id, renvoyant le prix le plus cher et la somme totale d'unité en notre possession

    Returns:
        list: (int) crypto_id, (float) price, (int) quantity
    """    
    connection = get_connection()
    cursor = connection.cursor()
    # récupération des id et prix dans la base de donnée
    cursor.execute("SELECT crypto_id, max(price) price, sum(quantity) quantity FROM crypto_value group by crypto_id order by crypto_id")
    data_from_local_database = cursor.fetchall()

    return data_from_local_database

def insert_new_crypto_quantity(cryptomonnaie_id, cryptomonnaie_quantity, cryptomonnaie_name, cryptomonnaie_unique_price) -> None:
    """ Insertion des valeurs dans la table crypto_value

    Args:
        cryptomonnaie_id (int): Identifiant unique de la cryptomonnaie fournit par l'api
        cryptomonnaie_quantity (int): quantité renseignée
        cryptomonnaie_name (str): nom de la cryptomonnaie fournit par l'api
        cryptomonnaie_unique_price (float): valeur unitaire de la crypto lors de l'achat
        
    Returns:
        None
    """    
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO crypto_value (crypto_id, name, price, quantity, date) VALUES (?, ?, ?, ?, ?)",(cryptomonnaie_id, cryptomonnaie_name,cryptomonnaie_unique_price, cryptomonnaie_quantity, date.today()))
    get_connection.commit()
    flash("Transaction Validée", "success")
    cursor.close()
    
def delete_crypto(cryptomonnaie_id) :
    """Suppression d'une cryptomonnaie dans la base de donnée sqlite

    Args:
        cryptomonnaie_id (int): Code unique de la cryptomonnaie fournit par l'api
        
    Returns : 
        None
    """    
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM crypto_value WHERE crypto_id = ?', (cryptomonnaie_id,))
    connection.commit()

def update_crypto(cryptomonnaie_id, cryptomonnaie_quantity) :
    """Mise à jour de la quantité de cryptomonnaie concerné 

    Args:
        cryptomonnaie_id (int): Identifiant unique de la cryptomonnaie fournit par l'api
        cryptomonnaie_quantity (int): Nouvelle quantité renseignée
    
    Returns : 
        None
    """    
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
    
def insert_amount_in_database(amount) :
    """Insertion de la valorisation dans la table evolution_gain

    Args:
        amount (float): valorisation des cryptos présente en base 
    
    Returns :
        None
    """    
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO evolution_gain (value, date) VALUES (?, ?)",
                    (amount, date.today())
                )
    connection.commit()
    connection.close()
    
def get_amount() -> list :
    """Retourne l'ensemble des valorisations de la table evolution_gain trié par date
    Returns:
        list: (date) date, (float) value 
    """    
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT date, value FROM evolution_gain ORDER BY Date')
    data = cursor.fetchall()
    connection.close()
    return data