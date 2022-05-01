import base64
from io import BytesIO

from matplotlib.figure import Figure
import numpy as np

from ..app import get_all_amount_from_database

# Définition de la couleur du graphique
axis_color = 'white'

def get_amount_chart() -> str :
    """
    Génération des datas en base64 du graphique d'investissement.
    Je récupère les données de la base de donnée et je génère un .png en base64
    afin de pouvoir ensuite l'envoyer à ma view
    Returns:
        string: base64 string image
    """    
    fig = Figure(facecolor='white')
    ax = fig.subplots()
    data = get_all_amount_from_database()
    
    axis_date= [date for date,value in data]
    ordonnee_valeurs  = [value for date,value in data]
    
    ax.plot(axis_date, ordonnee_valeurs ,'wo-')
    
    # style des axes
    ax.tick_params(color=axis_color, labelcolor=axis_color)
    ax.spines['bottom'].set_color(axis_color)
    ax.spines['left'].set_color(axis_color)
    
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 4))
    ax.set_ylabel('valorisation')     
    ax.xaxis.label.set_color(axis_color)
    ax.yaxis.label.set_color(axis_color)
    
    for x,y in zip(axis_date, ordonnee_valeurs):
        label = "{:.2f}".format(y)
        ax.annotate(
            label, 
            (x,y), 
            textcoords="offset points", 
            xytext=(10,15),
            color=axis_color,
            ha='center') 

    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data
