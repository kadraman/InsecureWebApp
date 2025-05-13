from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

from iwa.auth import routes