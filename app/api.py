import logging
import os

from flask import Blueprint, Response, json, request
from flask_cors import cross_origin
from flask import current_app

from .db import get_db

logger = logging.getLogger(__name__)

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/subscribe-user", methods=['POST'])
@cross_origin()
def subscribe_user():
    """Subscribe a user to the newsletter by writing to the JSON file"""
    if (os.environ.get('FORTIFY_IF_DJANGO')):
        id = request.POST['id', '']
        name = request.POST['name', '']
        email = request.POST['email', '']
        role = request.POST['role', 'ROLE_GUEST']
    else:    
        content = request.get_json('id')
        id = content['id']
        name = content['name']
        email = content['email']
        role = content['role']
    logger.debug(f"Registering user: {id},{name},{email},{role}")
    with open(current_app.config['SUBSCRIBERS_FILENAME'], mode='a+', encoding='utf-8') as f:
        try: 
            entries = json.load(f)
        except ValueError: 
            entries = []
        entry = {'id': id, 'name': name, 'email': email, 'role' : role}
        entries.append(entry)
        json.dump(entries, f)
        r = Response(json.dumps({'message': 'Successfully registered user'}), mimetype='application/json')
        r.status_code = 200
    return r