import json
import os
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from ..resources import cache

session = Session()
session.headers.update({
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.getenv("API_KEY_COIN")
})  
# Url de production
base_url = 'https://pro-api.coinmarketcap.com'

@cache.cached(timeout=18000, key_prefix='all_crypto')
def get_all_actual_crypto() -> json :
    """ Récupération de la liste des cryptocurrency à la mode actuellement
        Effectue l'appel sur l'api et récupère le résultat au format json pour traitement
    Returns:
        json: Récupération des 50 cryptomonnaies de l'api
    """  
    url = base_url+'/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'50',
        'convert': 'EUR'
    }
    try :
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except(ConnectionError, Timeout, TooManyRedirects) as error : 
        print(error)
