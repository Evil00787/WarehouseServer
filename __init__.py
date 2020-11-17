import os

import firebase_admin
from firebase_admin import credentials
from flask import Flask
from .db import products_db_req, auth_db_req
from flask_login import (
    LoginManager,
)
from pymongo import MongoClient
from .routes import auth as auth_blueprint
from .routes import main as main_blueprint

SECRET = os.environ.get("SECRET", None)
cred = credentials.Certificate("D:\\key\\firebase_admin.json")

default_app = firebase_admin.initialize_app(cred)
app = Flask(__name__)
login_manager = LoginManager()
clientProducts = MongoClient(port=27017)
app.db = clientProducts.IUMWarehouse
app.register_blueprint(auth_blueprint.authb)
app.register_blueprint(main_blueprint.mainb)
app.secret_key = SECRET
app.config['SESSION_TYPE'] = 'mongodb'
products_db_req.products = app.db.Products
auth_db_req.users = app.db.Users
login_manager.init_app(app)


@login_manager.user_loader
def load_user(uid):
	return auth_db_req.get_user_by_id(uid)


def get_app():
	return app
