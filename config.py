"""
Application configuration settings
"""
import os

class Config:
    """
    Common configurations
    """ 
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DBNAME = os.environ.get("DBNAME")
    DBUSER = os.environ.get("DBUSER")
    DBPASSWORD = os.environ.get("DBPASSWORD")

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True

class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    DBNAME = "testdb"

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}