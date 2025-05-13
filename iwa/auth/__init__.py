from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder='templates')

from iwa.auth import routes