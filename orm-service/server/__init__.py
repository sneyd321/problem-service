
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from firebase_admin import credentials, storage
import firebase_admin

import pymysql
pymysql.install_as_MySQLdb()

cred = credentials.Certificate(r'server/static/ServiceAccount.json')
firebase_admin.initialize_app(cred, {'storageBucket' : 'roomr-222721.appspot.com'})

bucket = storage.bucket()

db = SQLAlchemy()

from celery import Celery
ccc = Celery("server", broker='amqp://', backend='rpc://')


app = Flask(__name__)

c = Celery("server", broker='amqp://guest:guest@192.168.0.115:5672/')
c.config_from_object('celeryconfig')


def create_app(env):
    #Create app
    global app
    config = Config(app)
    if env == "prod":
        app = config.productionConfig()
    elif env == "dev":
        app = config.developmentConfig()
    elif env == "test":
        app = config.testConfig()
    else:
        return 
    

    
    migrate = Migrate(app, db)
    db.init_app(app)
    
    #Intialize modules
    from server.api.routes import problem
    app.register_blueprint(problem, url_prefix="/problem/v1")
    return app