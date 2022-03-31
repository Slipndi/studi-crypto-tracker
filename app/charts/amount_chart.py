import base64
from io import BytesIO
from matplotlib.figure import Figure
from ..db import get_amount

axis_color = 'white'

def get_amount_chart() :
    fig = Figure(facecolor='white')
    ax = fig.subplots()
    data = get_amount()
    ax.plot([date for date,value in data], [value for date,value in data], color=axis_color)
    # style des axes
    ax.tick_params(color=axis_color, labelcolor=axis_color)
    ax.spines['bottom'].set_color(axis_color)
    ax.spines['left'].set_color(axis_color)
    
    ax.set_xlabel('date')
    ax.set_ylabel('valorisation')     
    ax.xaxis.label.set_color(axis_color)
    ax.yaxis.label.set_color(axis_color)

    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data