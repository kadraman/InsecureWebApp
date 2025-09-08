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
import logging
import pickle
import pyotp

from flask import abort, flash, g, make_response, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from iwa.utils.db_utils import load_logged_in_user
from iwa.utils.view_utils import gen_login_cookie, login_required

from iwa.blueprints.auth import auth_bp
from iwa.repository.db import get_db


logger = logging.getLogger(__name__)


@auth_bp.route("/register", methods=("GET", "POST"))
def register():
    """
    Register a new user. Validates that the email is not
    already taken. Hashes the password for security.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (email, password) VALUES (?, ?)",
                    (email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                # The email was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {email} is already registered."
            else:
                # Success, go to the login page.
                flash('You have been successfully registered', 'success')
                return redirect(url_for("auth.login"))

        flash(error, 'error')

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    """
    Log in a registered user. If "rememberme" session cookie
    was set then auto login. If not then validate email
    and password credentials and redirect to OTP authentication
    if required.
    """
    errors = {}

    if 'rememberme' in request.cookies:
        # found 'rememberme' cookie, extract its details
        b64 = request.cookies.get('rememberme')
        a = pickle.loads(base64.b64decode(b64))
        # store the email in a new session and navigate to users home
        session.clear()
        session["email"] = a.email
        session['loggedin'] = True
        return redirect(url_for("users.home"))
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        logger.debug(f"Logging in user {email}:{password}")
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()

        if user is None:
            errors['email'] = "Incorrect email address."
        elif not check_password_hash(user["password"], password):
            errors['password'] = "Incorrect password."

        if not errors:
            # store the email in a new session and navigate to home
            session.clear()
            session["firstname"] = user["first_name"]
            session["lastname"] = user["last_name"]
            session["email"] = user["email"]
            session["password"] = user["password"]
            session["otp_enabled"] = 0
            if user["otp_enabled"]:
                load_logged_in_user()
                session["otp_enabled"] = 1
                return redirect(url_for("auth.verify_2fa"))
            else:
                session['loggedin'] = True
                return gen_login_cookie("rememberme", "users/home.html")
                #return redirect(url_for("users.home"))

        #flash(error, 'error')

    return render_template("auth/login.html", errors=errors, email=request.form.get("email", ""))


@auth_bp.route("/verify_2fa", methods=("GET", "POST"))
@login_required
def verify_2fa():
    """
    Requests a TOTP code to confirm the users login.
    """
    errors = {}

    if not session['otp_enabled']:
        abort(500, "2FA is not enabled.")

    load_logged_in_user()
    logger.debug(f"verify_2fa:: OTP secret for {g.user['email']} is {g.user['otp_secret']}")

    if request.method == "POST":
        # retrieve secret for the user  
        secret = g.user['otp_secret']
        otp = request.form["otp"]

        if not otp:
            errors['otp'] = "An OTP is required."
        else:
            totp = pyotp.TOTP(secret)
            if totp.verify(otp):
                # Success, go to the users home page
                session['loggedin'] = True
                return gen_login_cookie("rememberme", "users/home.html")
                #return redirect(url_for("users.home"))
            else:
                # Invalid OTP, try again
                errors['otp'] = "The OTP is invalid, please try again."

        #flash(error, 'error')

    return render_template("auth/verify_2fa.html", errors=errors,
                           otp_secret=g.user['otp_secret'])


@auth_bp.route("/logout")
def logout():
    """
    Clear the current session, including the stored user id.
    """
    session.clear()
    resp = make_response(redirect(url_for("main.index")))
    resp.set_cookie("rememberme", "", expires=0)
    return resp
