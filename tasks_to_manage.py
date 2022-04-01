import app.app as app

def scheduled_job():
    """Tache plannifiée une fois par jour, 
        Récupération des cryptomonnaies en base de données avec l'ensemble des détails
        calcul de la rentabilité actuelle
        insertion en base de donnée chaque action est découpée dans une fonctionnalité 
        dans main.
    """    
    cryptomonaies = app.get_crypto_from_database_with_details()
    amount = app.get_amount(cryptomonaies)
    app.insert_amount_in_database(amount)
    
scheduled_job()    