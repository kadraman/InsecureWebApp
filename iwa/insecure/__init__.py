from flask import Blueprint

insecure_bp = Blueprint("insecure", __name__, template_folder='templates')

from iwa.insecure import routes