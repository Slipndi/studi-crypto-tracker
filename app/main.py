
from re import X
from secrets import token_urlsafe
from flask import Flask, flash, render_template, redirect, request
from flask_wtf.csrf import CSRFProtect
from datetime import date


from .api_money import get_all_actual_crypto
from .db import get_crypto_in_database, get_connection
from .resources import cache

app = Flask(__name__)
secret = token_urlsafe(32)
app.secret_key = secret

csrf = CSRFProtect(app)
cache.init_app(app)

@app.route("/", methods=['GET'])
def home() -> render_template:
    cryptomonaies = get_crypto_from_database_with_details();
    amount = 0
    for crypto_api, price_compare, actual_price, quantity in cryptomonaies :
        amount += price_compare * quantity
    return render_template('crypto/index.html', cryptomonnaies=cryptomonaies, amount=amount)

@app.route('/remove', methods=['GET','POST'])
def remove_value_crypto() -> render_template :
    return render_template()

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

    # insertion en base de donnée
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO crypto_value (crypto_id, name, price, quantity, date) VALUES (?, ?, ?, ?, ?)",(cryptomonnaie_id, cryptomonnaie_name,cryptomonnaie_unique_price, cryptomonnaie_quantity, date.today()))
        cursor.commit()
        flash("Transaction Validée", "success")
        connection.close()
        return home()
    except Exception as e:
        flash(e, "error")
        return redirect(request.url)

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
