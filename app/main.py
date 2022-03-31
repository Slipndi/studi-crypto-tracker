from flask import Flask
from flask_caching import Cache
import db

app = Flask(__name__)
cache = Cache(app)

@app.route("/")
def home() :
    return "<h1>Home - test</h1>"