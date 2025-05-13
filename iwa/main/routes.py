    
import logging
import os
from flask import Blueprint, abort, send_file
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from iwa.main import main_bp
from iwa.products.repository import get_product, get_product_by_code, get_products, get_product_reviews

from iwa.repository import db

logger = logging.getLogger(__name__)


@main_bp.route("/")
def index():
    """
    Show the home page.
    """
    return render_template("main/index.html")



@main_bp.route("/reset-db")
def reset_db():
    """
    Reset the database to its initial state.
    """
    logger.debug("[reset_db] Re-initializing database.")
    db.init_db()
    return redirect(url_for("products.index"))