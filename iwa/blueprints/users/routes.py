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
from flask import flash, redirect, request, g, render_template, session, url_for

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
    return render_template("users/home.html", user=g.user)


@users_bp.route("/profile")
@login_required
def profile():
    """
    Show the users profile page.
    """
    return render_template("users/profile.html", user=g.user)


@users_bp.route("/update_profile", methods=("GET", "POST"))
@login_required
def update_profile():
    """
    Edit the users profile.
    """
    if request.method == "POST":
        email = session["email"]
        # TODO: implement update profile
        flash('Updating profile has not yet been implemented.', 'info')

    return render_template("users/profile.html", user=g.user)


@users_bp.route("/messages")
@login_required
def messages():
    """
    Show the users message page.
    """
    return render_template("users/messages.html", user=g.user)


@users_bp.route("/reviews")
@login_required
def reviews():
    """
    Show the users orders page.
    """
    return render_template("users/reviews.html", user=g.user)


@users_bp.route("/orders")
@login_required
def orders():
    """
    Show the users orders page.
    """
    return render_template("users/orders.html", user=g.user)


@users_bp.route("/security", methods=("GET", "POST"))
@login_required
def security():
    """
    Display and update the users security configuration.
    """

    if request.method == "POST":
        # Handle form submission for enabling/disabling 2FA
        if request.form.get('enable_otp'):
            logger.debug("Enabling two-factor authentication (2FA) for user")
            # User wants to enable 2FA
            if g.user['otp_enabled']:
                flash('Two-factor authentication is already enabled.', 'info')
            else:
                # Generate and store a secret for the user  
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
                # Success, redirect back to security page
                flash('Two-factor authentication has been successfully enabled.', 'success')
                return redirect(url_for("users.security"))

        elif request.form.get('disable_otp'):
            logger.debug("Disabling two-factor authentication (2FA) for user")
            # User wants to disable 2FA
            if not g.user['otp_enabled']:
                flash('Two-factor authentication is already disabled.', 'info')
            else:
                db = get_db()
                db.execute(
                    "UPDATE users SET otp_enabled=?, otp_secret=? WHERE email=?",
                    (0, None, g.user['email']),
                )
                db.commit()
                load_logged_in_user()
                # Success, redirect nack to security page
                flash('Two-factor authentication has been successfully disabled.', 'success')
                return redirect(url_for("users.security"))

    secret = g.user['otp_secret'] if g.user['otp_enabled'] else None

    if secret:
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

    qr_b64 = base64.b64encode(buffered.getvalue()).decode() if secret else None

    return render_template("users/security.html", user=g.user, qr_b64=qr_b64, secret=secret)


@users_bp.before_request
def load_logged_in_user():
    """If a email is stored in the session, load the user object from
    the database into ``g.user``."""
    email = session.get("email")
    if email is None:
        g.user = None
        logger.debug("No user is logged in.")
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        )
        logger.debug(f"Loading logged in user {g.user['email']}")
