import base64
import functools
from io import BytesIO
import logging
import os

from flask import Blueprint, Response, json
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import pyotp
import qrcode
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask import current_app

from ..repository.db import get_db

logger = logging.getLogger(__name__)

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        )
        logger.debug(f"Logged in user {g.user['email']}")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        logger.info(f"Logging in user {username}:{password}")
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and navigate to dashboard
            session.clear()
            session["user_id"] = user["id"]
            if user["otp_enabled"]:
                return redirect(url_for("auth.verify_2fa"))
            else:
                return redirect(url_for("dashboard"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/enable_2fa", methods=("GET", "POST"))
@login_required
def enable_2fa():
    if g.user['otp_enabled']:
        # 2FA is already enabled
        secret = g.user['otp_secret']
    else:
        # Generate and store a secret for the user  
        secret = pyotp.random_base32()
        db = get_db()
        error = None
        db.execute(
            "UPDATE users SET otp_enabled=?, otp_secret=? WHERE id=?",
            (1, secret, g.user['id']),
        )
  
    # Generate a QR code for the user to scan
    totp = pyotp.TOTP(secret)
    qr_url = totp.provisioning_uri(g.user['username'], issuer_name="InsecureWebApp")

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

    return render_template("auth/enable_2fa.html", qr_b64=qr_b64, secret=secret)


@bp.route("/verify_2fa", methods=("GET", "POST"))
@login_required
def verify_2fa():
    if not g.user['otp_enabled']:
        return "2FA is not enabled.", 400

    if request.method == "POST":
        # retrieve secret for the user  
        secret = g.user['otp_secret']
        otp = request.form["otp"]
        error = None

        if not otp:
            error = "OTP is required."

        if error is None:
            totp = pyotp.TOTP(secret)
            if totp.verify(otp):
                # Success, go to the dashboard.
                return redirect(url_for("dashboard"))
            else:
                # Invalid OTP, try again/
                error = "The OTP is invalid, please try again."

        flash(error)

    return render_template("auth/verify_2fa.html")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
