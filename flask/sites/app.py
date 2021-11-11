
from typing import Any
from flask import Flask
import os



def create_app():

    app: Any = Flask(__name__)

    #SECRET_KEY
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['DEBUG'] = True

    #Flask Config
    app.config.from_object('config.config.Config')

    return app

app = create_app()

