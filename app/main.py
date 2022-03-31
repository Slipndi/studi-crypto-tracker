
from re import X
from secrets import token_urlsafe
from flask import Flask, flash, render_template, redirect, request
from flask_wtf.csrf import CSRFProtect
from datetime import date
from .charts import get_amount_chart


from .api_money import get_all_actual_crypto
from .db import get_crypto_in_database, insert_new_crypto_quantity, delete_crypto, update_crypto
from .resources import cache

app = Flask(__name__)
# Génération d'une clef d'application
secret = token_urlsafe(32)
app.secret_key = secret
# Je rends le CSRF plus permissif car je rencontre des bugs aléatoire sur Heroku
app.config["WTF_CSRF_SSL_STRICT"]=False
# Activation de la protection CSRF
csrf = CSRFProtect(app)

# Activation du cache
cache.init_app(app)

@app.route("/", methods=['GET'])
def home() -> render_template:
    cryptomonaies = get_crypto_from_database_with_details();
    amount = get_amount(cryptomonaies)
    return render_template('crypto/index.html', cryptomonnaies=cryptomonaies, amount=amount)

@app.route('/remove', methods=['GET','POST'])
def remove_value_crypto() -> render_template :
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
    chart = get_amount_chart()
    return render_template('crypto/amount.html', chart=chart)


def get_crypto_from_database_with_details() -> list :
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
                cryptomonaies.append([crypto_api, price_compare, actual_price, quantity])
    return cryptomonaies

def get_amount(cryptomonaies) :
    amount=0
    for crypto_api, price_compare, actual_price, quantity in cryptomonaies :
        amount += price_compare * quantity
    return amount