import logging

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import pyotp
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from iwa.utils.ViewUtils import login_required

from ..repository.db import get_db

logger = logging.getLogger(__name__)

bp = Blueprint("auth", __name__, url_prefix="/auth")


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
                flash('You have been successfully registered', 'success')
                return redirect(url_for("auth.login"))

        flash(error, 'error')

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
            # store the user id in a new session and navigate to home
            session.clear()
            session["user_id"] = user["id"]
            if user["otp_enabled"]:
                return redirect(url_for("auth.verify_2fa"))
            else:
                return redirect(url_for("user.home"))

        flash(error, 'error')

    return render_template("auth/login.html")


@bp.route("/verify_2fa", methods=("GET", "POST"))
@login_required
def verify_2fa():
    """Requests a TOTP code to confirm login"""
    if not g.user['otp_enabled']:
        return "2FA is not enabled.", 400

    if request.method == "POST":
        # retrieve secret for the user  
        secret = g.user['otp_secret']
        otp = request.form["otp"]
        error = None

        if not otp:
            error = "An OTP is required."

        if error is None:
            totp = pyotp.TOTP(secret)
            if totp.verify(otp):
                # Success, go to the home.
                return redirect(url_for("user.home"))
            else:
                # Invalid OTP, try again/
                error = "The OTP is invalid, please try again."

        flash(error, 'error')

    return render_template("auth/verify_2fa.html", otp_secret=g.user['otp_secret'])


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
