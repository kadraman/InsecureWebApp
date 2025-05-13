import base64
from io import BytesIO
import logging
import pyotp
import qrcode
from flask import Blueprint, flash, request, g, render_template, session

from iwa.users import users_bp
from iwa.utils.db_utils import load_logged_in_user
from iwa.utils.view_utils import login_required

from ..repository.db import get_db

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
        username = session["username"]
        secret = pyotp.random_base32()
        db = get_db()
        error = None
        db.execute(
            "UPDATE users SET otp_enabled=?, otp_secret=? WHERE username=?",
            (1, secret, username),
        )
        db.commit()
        load_logged_in_user()

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

    return render_template("users/security.html", user=g.user, qr_b64=qr_b64, secret=secret)


@users_bp.route("/update_security", methods=("GET", "POST"))
@login_required
def update_security():
    """
    Edit the users security details.
    """
    if request.method == "POST":
        username = session["username"]
        # TODO: implement update security
        flash('Updating security details has not yet been implemented.', 'info')

    return render_template("users/update_security.html", user=g.user)


@users_bp.before_request
def load_logged_in_user():
    """If a username is stored in the session, load the user object from
    the database into ``g.user``."""
    username = session.get("username")
    if username is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
       )
    logger.debug(f"Loading logged in user {g.user['username']}")
