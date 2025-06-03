from flask import Flask
from . import urlshort

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key='abdakjdbskj'

    
    app.register_blueprint(urlshort.bp)

    return app