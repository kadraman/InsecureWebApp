from flask import Blueprint

api_bp = Blueprint("api", __name__)

from iwa.api import routes