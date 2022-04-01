import app.main as main

def scheduled_job():
    cryptomonaies = main.get_crypto_from_database_with_details()
    amount = main.get_amount(cryptomonaies)
    main.insert_amount_in_database(amount)
    
scheduled_job()    