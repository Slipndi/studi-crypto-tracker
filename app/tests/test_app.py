from run import app
import app.app as a
from decimal import Decimal
    

def test_should_get_status_code_ok_on_index(client):
    """ test que la route / existe bien et ne renvoi pas de code erreur

    Args:
        client (app): contexte d'application
    """
    response = client.get('/')
    assert response.status_code == 200

def test_should_get_status_code_ok_on_remove(client):
    """ Vérifie que la page /remove existe

    Args:
        client (app): context d'application
    """
    response = client.get('/remove')
    assert response.status_code == 200
    
def test_should_get_status_code_ok_on_add(client):
    """ Vérifie que la page /add existe

    Args:
        client (app): context d'application
    """
    response = client.get('/add')
    assert response.status_code == 200
    
def test_should_get_status_code_ok_on_amount_graph(client):
    """ Verifie que la page /amount-graph existe

    Args:
        client (app): context d'application
    """
    response = client.get('/amount-graph')
    assert response.status_code == 200

def test_should_get_all_amount_from_database_return_list():
    """ Vérifie que get_all_amount_from_database renvoi bien une liste
    """
    result = a.get_all_amount_from_database()
    assert isinstance(result, list)
    
def test_should_get_crypto_in_database_return_list():
    """ Vérifie que get_crypto_in_database renvoi bien une liste
    """
    result = a.get_crypto_in_database()
    assert isinstance(result, list)

def test_get_amount_return_right_amount():
    """ Vérifie que get_amount renvoi le bon montant
    """
    result = a.get_amount([[10, -10.20, 27.18, 30], [25, 20.20, 27.20, 30 ]])
    assert result==300.0