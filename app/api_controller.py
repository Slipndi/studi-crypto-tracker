from app.api_keys import API_KEY_COINMARKET
from requests import Session, Request
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


# Url de production
base_url = 'https://pro-api.coinmarketcap.com'

# URL bac à sable pour les tests 
# base_url= 'https://sandbox-api.coinmarketcap.com'

# Création de la session avec le header et la clef API
session = Session()
session.headers.update({
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY_COINMARKET
})


def get_all_actual_crypto() -> json :
    ''' 
        Récupération de la liste des cryptocurrency à la mode actuellement
        Effectue l'appel sur l'api et récupère le résultat au format json pour traitement
    '''
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
