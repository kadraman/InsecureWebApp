from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint("products", __name__)


@bp.route("/")
def index():
    """Show all the products, most recent first."""
    db = get_db()
    products = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM product p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", products=products)


def get_product(id, check_author=True):
    """Get a product and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of product to get
    :param check_author: require the current user to be the author
    :return: the product with author information
    :raise 404: if a product with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    product = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM product p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if product is None:
        abort(404, f"product id {id} doesn't exist.")

    if check_author and product["author_id"] != g.user["id"]:
        abort(403)

    return product


@bp.route("/create", methods=("GET", "POST"))
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
                "INSERT INTO product (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
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
                "UPDATE product SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", product=product)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a product.

    Ensures that the product exists and that the logged in user is the
    author of the product.
    """
    get_product(id)
    db = get_db()
    db.execute("DELETE FROM product WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))