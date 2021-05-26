from unittest import TestCase
from flask import current_app
from app import app 
from config import CONFIG as app_config
from app.v2.models import User, Ride

class BaseTest(TestCase):
    def setUp(self):

        app.config.from_object(app_config['testing'])
        self.app = app.test_client()
        ctx = app.app_context()
        ctx.push()


        self.user = {
	"name": "root",
	"username": "sammy",
	"email": "sammy@gmail.com",
	"password": "groot"
        }
        user = User()
        user.drop('users')
        user.create()
        ride = Ride()
        user.drop('rides')
        ride.create()
        
