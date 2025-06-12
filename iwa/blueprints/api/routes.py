"""
        InsecureWebApp - an insecure Python/Flask Web application

        Copyright (C) 2024-2025  Kevin A. Lee (kadraman)

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging

from flask import Response, json, request
from flask_cors import cross_origin
from flask import current_app

from iwa.blueprints.api import api_bp
from iwa.repository.db import get_db


logger = logging.getLogger(__name__)


@api_bp.route("/subscribe-user", methods=['POST'])
@cross_origin()
def subscribe_user():
    """Subscribe a user to the newsletter by writing to the JSON file"""    
    content = request.json
    id = content.get('id')
    name = content.get('name')
    email = content.get('email')
    role = content.get('role')
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


@api_bp.route("/new-products", methods=['GET'])
@cross_origin()
def new_products():  
    limit = request.args.get('limit', 3)  

    """Get 'limit' products, ordered by name."""
    db = get_db()
    products = db.execute(
        "SELECT *"
        " FROM products p"
        " ORDER BY name"
        " LIMIT ?", (limit,)
    ).fetchall()
    r = Response(json.dumps([dict(ix) for ix in products]), mimetype='application/json')
    r.status_code = 200
    return r