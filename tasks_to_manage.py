import app.main as main

def scheduled_job():
    """Tache plannifiée une fois par jour, 
        Récupération des cryptomonnaies en base de données avec l'ensemble des détails
        calcul de la rentabilité actuelle
        insertion en base de donnée chaque action est découpée dans une fonctionnalité 
        dans main.
    """    
    cryptomonaies = main.get_crypto_from_database_with_details()
    amount = main.get_amount(cryptomonaies)
    main.insert_amount_in_database(amount)
    
scheduled_job()    