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

import base64
from io import BytesIO
import logging
import pyotp
import qrcode
from flask import flash, request, g, render_template, session

from iwa.blueprints.users import users_bp
from iwa.utils.db_utils import load_logged_in_user
from iwa.utils.view_utils import login_required
from iwa.repository.db import get_db


logger = logging.getLogger(__name__)


@users_bp.route("/home")
@login_required
def home():
    """
    Show the users home page.
    """
    return render_template("users/home.html")


@users_bp.route("/profile")
@login_required
def profile():
    """
    Show the users profile page.
    """
    return render_template("users/profile.html")


@users_bp.route("/messages")
@login_required
def messages():
    """
    Show the users message page.
    """
    return render_template("users/messages.html")


@users_bp.route("/reviews")
@login_required
def reviews():
    """
    Show the users orders page.
    """
    return render_template("users/reviews.html")


@users_bp.route("/orders")
@login_required
def orders():
    """
    Show the users orders page.
    """
    return render_template("users/orders.html")


@users_bp.route("/security", methods=("GET", "POST"))
@login_required
def security():
    """
    Display and update the users security configuration.
    """
    if g.user['otp_enabled']:
        # 2FA is already enabled
        secret = g.user['otp_secret']
    else:
        # Generate and store a secret for the user  
        #user_id: int = session["user_id"]
        email = session["email"]
        secret = pyotp.random_base32()
        db = get_db()
        error = None
        db.execute(
            "UPDATE users SET otp_enabled=?, otp_secret=? WHERE email=?",
            (1, secret, email),
        )
        db.commit()
        load_logged_in_user()

    # Generate a QR code for the user to scan
    totp = pyotp.TOTP(secret)
    qr_url = totp.provisioning_uri(g.user['email'], issuer_name="InsecureWebApp")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code to base64 for display
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    qr_b64 = base64.b64encode(buffered.getvalue()).decode()

    return render_template("users/security.html", user=g.user, qr_b64=qr_b64, secret=secret)


@users_bp.route("/update_security", methods=("GET", "POST"))
@login_required
def update_security():
    """
    Edit the users security details.
    """
    if request.method == "POST":
        email = session["email"]
        # TODO: implement update security
        flash('Updating security details has not yet been implemented.', 'info')

    return render_template("users/update_security.html", user=g.user)


@users_bp.before_request
def load_logged_in_user():
    """If a email is stored in the session, load the user object from
    the database into ``g.user``."""
    email = session.get("email")
    if email is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
       )
    logger.debug(f"Loading logged in user {g.user['email']}")
