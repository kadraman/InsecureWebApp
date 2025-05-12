import logging

from werkzeug.exceptions import abort

from ..repository.db import get_db
from ..models.Product import Product
from ..models.Review import Review

logger = logging.getLogger(__name__)

def get_products(keywords):
    """Get products, ordered by name

    :param keywords: product names to filter on
    :return: collection of products
    """
    data = (
        get_db()
        .execute(
            "SELECT *"
            " FROM products p"
            " WHERE name LIKE '%%" + keywords + "%%'"
            " ORDER BY name"
        )
        .fetchall()
    )

    return data

def get_product(id):
    """Get a product by id.

    Checks that the id exists.

    :param id: id of product to get
    :return: the product information
    :raise 404: if a product with the given id doesn't exist
    """
    data = (
        get_db()
        .execute(
            "SELECT *"
            " FROM products p"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if data is None:
        abort(404, f"product id {id} doesn't exist.")

    return Product(id=data[0], code=data[1], name=data[2], summary=data[3], description=data[4],
                           image=data[5], price=data[6], on_sale=data[7], sale_price=data[8], in_stock=data[9],
                           time_to_stock=data[10], rating=data[11], available=data[12])


def get_product_by_code(code):
    """Get a product by code.

    Checks that the code exists.

    :param code: code of product to get
    :return: the product information
    :raise 404: if a product with the given code doesn't exist
    """
    data = (
        get_db()
        .execute(
            "SELECT *"
            " FROM products p"
            " WHERE p.code = ?",
            (code,),
        )
        .fetchone()
    )

    if data is None:
        abort(404, f"product code {code} doesn't exist.")

    return Product(id=data[0], code=data[1], name=data[2], summary=data[3], description=data[4],
                           image=data[5], price=data[6], on_sale=data[7], sale_price=data[8], in_stock=data[9],
                           time_to_stock=data[10], rating=data[11], available=data[12])


def get_reviews(keywords):
    """Get reviews, ordered by date

    :param keywords: review contents to filter on
    :return: collection of reviews
    """
    data = (
        get_db()
        .execute(
            "SELECT *"
            " FROM reviews r"
            " WHERE content LIKE '%%" + keywords + "%%'"
            " ORDER BY date DESC"
        )
        .fetchall()
    )

    return data


def get_product_reviews(pid):
    """Get a product's reviews.

    Checks that the pid exists.

    :param pid: id of product to get
    :return: the review information
    :raise 404: if a product with the given id doesn't exist
    """
    db = get_db()
    data = db.execute(
        "SELECT r.user_id, r.review_date, r.comment, u.username"
        " FROM reviews r"
        " JOIN users u ON r.user_id = u.id AND"
        " (r.product_id = ? OR r.product_id IS null)",
        (pid,),
    ).fetchall()

    return data


def get_user_reviews(uid):
    """Get a user's reviews.

    Checks that the uid exists.

    :param uid: id of user to get reviews for
    :return: the review information
    :raise 404: if a user with the given id doesn't exist
    """
    db = get_db()
    data = db.execute(
        "SELECT r.user_id, r.review_date, r.comment, u.username"
        " FROM reviews r"
        " JOIN users u ON r.user_id = u.id AND"
        " (r.user_id = ? OR r.product_id IS null)",
        (uid,),
    ).fetchall()

    return data


def get_review(id):
    """Get a review by id.

    Checks that the id exists.

    :param id: id of review to get
    :return: the review information
    :raise 404: if a review with the given id doesn't exist
    """
    data = (
        get_db()
        .execute(
            "SELECT *"
            " FROM reviews r"
            " WHERE r.id = ?",
            (id,),
        )
        .fetchone()
    )

    if data is None:
        abort(404, f"review id {id} doesn't exist.")

    return Product(id=data[0], product_id=data[1], user_id=data[2], review_date=data[3], comment=data[4],
                           rating=data[5], visible=data[6])