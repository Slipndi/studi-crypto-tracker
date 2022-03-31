from flask import Flask, render_template
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect
from api.controllers import get_all_actual_crypto
from db.db import get_crypto_in_database

app = Flask(__name__)
cache = Cache(app)
csrf = CSRFProtect(app)

@app.route("/", methods=['GET'])
def home() -> render_template:
    cryptomonaies = get_crypto_from_database_with_details();
    amount = 0
    for crypto_api, price_compare, actual_price, quantity in cryptomonaies :
        amount += price_compare * quantity
            
    return render_template('crypto/index.html', cryptomonnaies=cryptomonaies, amount=amount)



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