
from secrets import token_urlsafe
from flask import Flask, flash, render_template, session
from flask_wtf.csrf import CSRFProtect


from .api_money import get_all_actual_crypto
from .db import get_crypto_in_database
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
    return render_template()

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
