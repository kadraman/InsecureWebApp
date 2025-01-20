import logging

from werkzeug.exceptions import abort

from .db import get_db
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

    #if data is None:
    #    abort(404, f"product id {id} doesn't exist.")

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


def get_reviews(id):
    """Get a product's reviews.

    Checks that the id exists.

    :param id: id of product to get
    :return: the review information
    :raise 404: if a product with the given id doesn't exist
    """
    db = get_db()
    data = db.execute(
        "SELECT r.user_id, r.review_date, r.comment, u.username"
        " FROM reviews r"
        " JOIN users u ON r.user_id = u.id AND"
        " (r.product_id = ? OR r.product_id IS null)",
        (id,),
    ).fetchall()

    #if data is None:
    #    abort(404, f"review id {id} doesn't exist.")

    return data