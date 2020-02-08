from flask import Blueprint,Flask
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)


v2 = Blueprint('v2',__name__)

from . import views