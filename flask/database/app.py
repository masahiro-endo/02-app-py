from flask import Flask
from core.database import init_db
import os
import logging

def create_app():

    app = Flask(__name__)

    #SECRET_KEY
    app.config['SECRET_KEY'] = os.urandom(24)

    #Flask Config
    app.config.from_object('config.config.Config')

    #sqlalchemy log setting
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)

    #database.py
    init_db(app)

    return app

app = create_app()

