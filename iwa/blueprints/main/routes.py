    
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
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from iwa.blueprints.main import main_bp
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