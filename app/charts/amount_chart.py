import base64
from io import BytesIO

from matplotlib.figure import Figure

from ..db import get_amount

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
    data = get_amount()
    ax.plot([date for date,value in data], [value for date,value in data], color=axis_color)
    # style des axes
    ax.tick_params(color=axis_color, labelcolor=axis_color)
    ax.spines['bottom'].set_color(axis_color)
    ax.spines['left'].set_color(axis_color)
    ax.set_ylabel('valorisation')     
    ax.xaxis.label.set_color(axis_color)
    ax.yaxis.label.set_color(axis_color)

    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data
