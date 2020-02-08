"""App entry point"""
from app.v2.models import User, Ride
from app import app

@app.cli.command()
def create():
    ''' Create all db tables '''
    User().create()
    Ride().create()
    