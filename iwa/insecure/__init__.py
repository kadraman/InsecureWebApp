from flask import Blueprint

insecure_bp = Blueprint("insecure", __name__)

from iwa.insecure import routes