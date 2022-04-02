from run import app
    
def test_should_get_status_code_ok_on_index(client):
    response = client.get('/')
    assert response.status_code == 200