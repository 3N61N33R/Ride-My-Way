from flask import Blueprint, Flask
from flasgger import Swagger

app2 = Flask(__name__)
Swagger(app2)


v2 = Blueprint("v2", __name__)

from . import views
