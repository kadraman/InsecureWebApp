from flask import Blueprint

api_bp = Blueprint("api", __name__, template_folder='templates')

from iwa.api import routes