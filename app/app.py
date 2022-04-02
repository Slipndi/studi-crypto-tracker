
import os

from datetime import date
from decimal import Decimal
from secrets import token_urlsafe

from flask import Flask, flash, redirect, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
import mysql.connector

app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE':'SimpleCache', 'CACHE_DEFAULT_TIMEOUT':18000})

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"), 
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)


# Génération d'une clef d'application
secret = token_urlsafe(32)
app.secret_key = secret
# Je rends le CSRF plus permissif car je rencontre des bugs aléatoire sur Heroku
app.config["WTF_CSRF_SSL_STRICT"]=False
app.config["WTF_CSRF_SECRET_KEY"]=os.getenv("API_KEY_COIN")
# Activation de la protection CSRF
csrf = CSRFProtect(app)
# Activation du cache
cache.init_app(app)



def csrf_error(reason):
    flash(reason, "error")
    return redirect(request.url)

def get_crypto_from_database_with_details() -> list :
    """Récupération de toutes les cryptomonnaies en base de donnée
    concaténation avec les informations nécessaires de l'api

    Returns:
        list: [ (int)crypto_api, (float) price_compare, (float) actual_price, (float) quantity]
    """    
    from .api_money import get_all_actual_crypto
    all_cryptomonnaies = get_all_actual_crypto()['data'] 
    data = get_crypto_in_database()
    cryptomonaies = []
    for crypto_api in all_cryptomonnaies :
        for crypto_id, price, quantity in data :
            if crypto_id == crypto_api['id'] :
                # récupération du prix actuel de la crypto
                actual_price = crypto_api['quote']['EUR']['price']
                # comparation des prix pour l'affichage de l'icone
                price_compare = actual_price - price
                # création d'un tableau unique pour faciliter le traitement dans la vue
                cryptomonaies.append([crypto_api, price_compare, actual_price, float(quantity)])
    return cryptomonaies

def get_amount(cryptomonaies : list) -> float :
    """
        Récupération de la valorisation actuelle de la cryptomonnaie selectionnée
    Args:
        cryptomonaies (list): [ (int)crypto_api, (float) price_compare, (float) actual_price, (float) quantity]

    Returns:
        float: valorisation calculé de la cryptomonnaie
    """    
    amount=0
    for crypto_api, price_compare, actual_price, quantity in cryptomonaies :
        amount += price_compare * quantity
    return amount

def get_crypto_in_database() -> list :
    """Récupération de toutes les cryptomonnaies insérées dans la table crypto_value
    groupées par leurs id, renvoyant le prix le plus cher et la somme totale d'unité en notre possession

    Returns:
        list: [ (int) crypto_id, (float) price, (int) quantity ]
    """    
    cursor = mydb.cursor()
    # récupération des id et prix dans la base de donnée
    cursor.execute("SELECT crypto_id, max(price) price, sum(quantity) quantity FROM crypto_value group by crypto_id order by crypto_id")
    return cursor.fetchall()

def insert_new_crypto_quantity(cryptomonnaie_id, cryptomonnaie_quantity, cryptomonnaie_name, cryptomonnaie_unique_price):
    """ Insertion des valeurs dans la table crypto_value

    Args:
        cryptomonnaie_id (int): Identifiant unique de la cryptomonnaie fournit par l'api
        cryptomonnaie_quantity (int): quantité renseignée
        cryptomonnaie_name (str): nom de la cryptomonnaie fournit par l'api
        cryptomonnaie_unique_price (float): valeur unitaire de la crypto lors de l'achat
        
    Returns:
        None
    """    
    cursor = mydb.cursor()
    cursor.execute('''INSERT INTO crypto_value (crypto_id, name, price, quantity, date) VALUES (%s, %s, %s, %s, %s)''',(cryptomonnaie_id, cryptomonnaie_name,cryptomonnaie_unique_price, cryptomonnaie_quantity, date.today()))
    mydb.commit()
    flash("Transaction Validée", "success")

def delete_crypto(cryptomonnaie_id) :
    """Suppression d'une cryptomonnaie dans la base de donnée sqlite

    Args:
        cryptomonnaie_id (int): Code unique de la cryptomonnaie fournit par l'api
        
    Returns : 
        None
    """    
    cursor = mydb.cursor()
    cursor.execute('DELETE FROM crypto_value WHERE crypto_id = %s', (cryptomonnaie_id,))
    mydb.commit()

def update_crypto(cryptomonnaie_id, cryptomonnaie_quantity) :
    """Mise à jour de la quantité de cryptomonnaie concerné 

    Args:
        cryptomonnaie_id (int): Identifiant unique de la cryptomonnaie fournit par l'api
        cryptomonnaie_quantity (int): Nouvelle quantité renseignée
    
    Returns : 
        None
    """    
    cursor = mydb.cursor()
    cursor.execute('''SELECT id, crypto_id,quantity FROM crypto_value WHERE crypto_id = %s ORDER BY Quantity, price ''', (cryptomonnaie_id,))
    query_result = cursor.fetchall()
        
    # si il existe qu'une ligne dans la base de donnée, on la met à jour
    if len(query_result) == 1 :
        new_quantity = query_result[0]['quantity'] - cryptomonnaie_quantity
        cursor.execute('''UPDATE crypto_value SET quantity = %s WHERE crypto_id = %s ''', (new_quantity, cryptomonnaie_id ))
        mydb.commit()
    else : 
    # Sinon on vérifie ligne par ligne et fait évoluer la quantité
        new_quantity = cryptomonnaie_quantity
        for id, crypto_id, quantity in query_result : 
            # tant que la nouvelle quantité est supérieur à 0
                if quantity <= new_quantity :
                    new_quantity -= quantity
                    cursor.execute('''DELETE FROM crypto_value where id =%s''', (id, ))
                    mydb.commit()
                else : 
                    new_quantity = quantity-new_quantity
                    cursor.execute('''UPDATE crypto_value SET quantity = %s WHERE crypto_id = %s ''', (new_quantity, cryptomonnaie_id ))
                    mydb.commit()
                    new_quantity=0
        flash("Mise à jour réussie", "success")
    
def insert_amount_in_database(amount) :
    """Insertion de la valorisation dans la table evolution_gain

    Args:
        amount (float): valorisation des cryptos présente en base 
    
    Returns :
        None
    """    
    cursor = mydb.cursor()
    cursor.execute('''INSERT INTO evolution_gain (value, date) VALUES (%s, %s)''',
                    (amount, date.today())
                )
    mydb.commit()
    
def get_all_amount_from_database() -> list :
    """Retourne l'ensemble des valorisations de la table evolution_gain trié par date
    Returns:
        list: (date) date, (float) value 
    """    
    cursor = mydb.cursor()
    cursor.execute('SELECT date, value FROM evolution_gain ORDER BY Date')
    return cursor.fetchall()

@app.route("/", methods=['GET'])
def home() -> render_template:
    """ Controller principale de la route /home
    récupération des informations et affichage sur la page principale de l'application

    Returns:
        render_template: renvoi le template templates/crypto/index.html
    """    
    cryptomonaies = get_crypto_from_database_with_details();
    amount = format(get_amount(cryptomonaies), '.4f')
    return render_template('crypto/index.html', cryptomonnaies=cryptomonaies, amount=amount)

@app.route('/remove', methods=['GET','POST'])
def remove_value_crypto() -> render_template :
    """ Affichage du formulaire en cas d'appel via la route GET
    Vérification du formulaire de suppression/update via la route POST

    Returns:
        render_template:    POST : templates/crypto/index.html
                            GET : templates/crypto/remove.html
    """    
    if request.method == 'GET':
        cryptomonnaies = get_crypto_from_database_with_details();
        return render_template('/crypto/remove.html', cryptomonnaies = cryptomonnaies)
        
    if request.method == 'POST':
        cryptomonnaie_id = int(request.values.get('cryptomonnaie'))
        cryptomonnaie_quantity = int(request.values.get('quantity'))
        # si la quantité est null ou inférieure à 0 erreur
        if cryptomonnaie_quantity == "" or cryptomonnaie_quantity < 0:
            flash("Quantité invalide", "error")
            return redirect(request.url)
        # si l'id n'est pas un entier positif
        if cryptomonnaie_id == "" or cryptomonnaie_id < 0:
            flash("Quantité invalide", "error")
            return redirect(request.url)
            
        all_crypto_in_database = get_crypto_in_database()
        quantity_available_in_database = [quantity for crypto_id, price, quantity in all_crypto_in_database if crypto_id == cryptomonnaie_id]
        if quantity_available_in_database[0] <= cryptomonnaie_quantity :
            try : 
                delete_crypto(cryptomonnaie_id)
                flash("Suppression réussie", "success")
            except Exception as e:
                flash(e, "error")
        else : 
            update_crypto(cryptomonnaie_id, cryptomonnaie_quantity)
        return home()

@app.route('/add', methods=['GET','POST'])
def add_new_crypto() -> render_template :
    """Ajouter une nouvelle cryptomonnaie renseignée dans la base de donnée
    la requête GET permet d'accéder au formulaire, la requête POST de traiter celui-ci
    
    Returns:
        render_template:    GET-> templates/crypto/add.html
                            POST-> templates/crypto/home.html
    """    
    from .api_money import get_all_actual_crypto
    cryptomonnaies = get_all_actual_crypto()
    if request.method == 'GET':
        return render_template('/crypto/add.html', cryptomonnaies=cryptomonnaies)

    cryptomonnaie_id = int(request.values.get('cryptomonnaie'))
    cryptomonnaie_quantity = int(request.values.get('quantity'))
    cryptomonnaie_value = float(request.values.get('euro_price'))
    cryptomonnaie_name = request.values.get('crypto_name')
    cryptomonnaie_unique_price = float(request.values.get('unique_price'))
    # validation du formulaire
    if cryptomonnaie_id == "":
        flash("Pas de cryptomonnaie", "error")
        return redirect(request.url)
    # si la quantité est null ou inférieure à 0 erreur
    if cryptomonnaie_quantity == "" or cryptomonnaie_quantity < 0:
        flash("Quantité invalide", "error")
        return redirect(request.url)
    
    # si le prix est null ou inférieure à 0 erreur
    if cryptomonnaie_value == "" or cryptomonnaie_value < 0:
        flash("Prix calculé invalide", "error")
        return redirect(request.url)
        
        # si le nom est null
    if cryptomonnaie_name == "":
        flash("Le nom de la crypto n'est pas renseigné", "error")
        return redirect(request.url)
    
    if cryptomonnaie_unique_price == "" or cryptomonnaie_unique_price < 0:
        flash("Le tarif unitaire n'est pas bon")
        return redirect(request.url)    
    ###################################
    try:
        insert_new_crypto_quantity(cryptomonnaie_id, cryptomonnaie_quantity, cryptomonnaie_name, cryptomonnaie_unique_price)
        return home()
    except Exception as e:
        flash(e, "error")
        return redirect(request.url)

@app.route('/amount-graph', methods=['GET'])
def display_amount_graph() -> render_template :
    """ Génération du graphique de valorisation et affichage sur le template

    Returns:
        render_template: templates/crypto/amount.html
    """    
    from .charts import get_amount_chart
    chart = get_amount_chart()
    return render_template('crypto/amount.html', chart=chart)