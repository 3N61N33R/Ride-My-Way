"""
Application package constructor
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from config import CONFIG
from .v2 import v2 as v2_blueprint
from app.v2.models import User, Ride

app = Flask(__name__)
jwt = JWTManager(app)

app.config.from_object(CONFIG['development'])
from . import routes


app.register_blueprint(v2_blueprint)