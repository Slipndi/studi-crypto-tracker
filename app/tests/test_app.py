from run import app
import app.app as a
    

def test_should_get_status_code_ok_on_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_should_get_status_code_ok_on_remove(client):
    response = client.get('/remove')
    assert response.status_code == 200
    
def test_should_get_status_code_ok_on_add(client):
    response = client.get('/add')
    assert response.status_code == 200
    
def test_should_get_status_code_ok_on_amount_graph(client):
    response = client.get('/amount-graph')
    assert response.status_code == 200

def test_should_get_all_amount_from_database_return_list():
    result = a.get_all_amount_from_database()
    assert isinstance(result, list)
