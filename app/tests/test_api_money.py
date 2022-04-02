import json
from app.api_money.controllers import get_all_actual_crypto
from run import app
import app.api_money 

def test_should_get_all_actual_crypto():
    result = get_all_actual_crypto()
    assert isinstance(result, dict)
