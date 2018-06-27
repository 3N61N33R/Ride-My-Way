"""
Application package constructor
"""
from flask import Flask

from config import CONFIG

def create_app(config_name):
    """
    Application Factory
    """
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])


    return app