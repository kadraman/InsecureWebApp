import logging
import os
from flask import Blueprint, abort, send_file
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from iwa.products import products_bp
from iwa.products.repository import get_product, get_product_by_code, get_products, get_product_reviews
from iwa.utils.ViewUtils import login_required
from ..repository.db import get_db

logger = logging.getLogger(__name__)


@products_bp.route("/")
def index():  
    keywords = request.args.get('keywords')
    if (keywords):
        logger.info(f"Searching for products with keywords: {keywords}")
    else:
        keywords=""    

    """Show all the products, ordered by name."""
    products = get_products(keywords)
    
    return render_template("products/index.html", products=products)


@products_bp.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):  
    logger.info(f"Downloading file: {filename}")
    """Download an artifact related to the product"""
    if not filename:
        abort(404, "File not specified")
    site_root = os.path.realpath(os.path.dirname(__file__))
    logger.info("Download path:" + os.path.join(site_root, "data", filename))
    return send_file(os.path.join(site_root, "data", filename), as_attachment=True)


@products_bp.route("/<string:code>/view")
def view(code):
    """View an individual product and its reviews"""
    product = get_product_by_code(code)
    reviews = get_product_reviews(product.id)
    return render_template("products/view.html", product=product, reviews=reviews)


"""The below are not yet used"""


@products_bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new product for the current user."""
    if request.method == "product":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO products (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("products.index"))

    return render_template("products/create.html")


@products_bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a product if the current user is the author."""
    product = get_product(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE products SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("products.index"))

    return render_template("products/update.html", product=product)


@products_bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a product.

    Ensures that the product exists and that the logged in user is the
    author of the product.
    """
    get_product(id)
    db = get_db()
    db.execute("DELETE FROM products WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("products.index"))