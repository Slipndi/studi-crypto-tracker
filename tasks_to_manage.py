from app.main import get_crypto_from_database_with_details, get_amount, insert_amount_in_database

def scheduled_job():
    cryptomonaies = get_crypto_from_database_with_details()
    amount = get_amount(cryptomonaies)
    insert_amount_in_database(amount)
    
scheduled_job()    