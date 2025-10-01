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

from iwa.blueprints.products import products_api_bp
from iwa.repository.db import get_db

logger = logging.getLogger(__name__)


@products_api_bp.route("/", methods=['GET'])
@cross_origin()
def search_products():
    """Search products by keyword in name or description."""
    keywords = request.args.get('keywords', '')
    db = get_db()
    query = "SELECT * FROM products WHERE name LIKE '%" + keywords + "%'"
    products = db.execute(query).fetchall()
    data = [dict(product) for product in products]
    r = Response(json.dumps(data), mimetype='application/json')
    r.status_code = 200
    return r

@products_api_bp.route("/<int:product_id>", methods=['GET'])
@cross_origin()
def products(product_id):
    """ Get product by id."""
    db = get_db()
    if product_id:
        product = db.execute(
            "SELECT * FROM products p WHERE p.id = ?", (product_id,)
        ).fetchone()
        logger.debug(product)
        data = dict(product) if product else {}
        r = Response(json.dumps(data), mimetype='application/json')
    else:
        # Return empty JSON object if no id is specified
        r = Response(json.dumps({}), mimetype='application/json')
    r.status_code = 200
    return r

@products_api_bp.route("/new-products", methods=['GET'])
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