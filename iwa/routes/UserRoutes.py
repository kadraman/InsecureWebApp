import base64
import functools
from io import BytesIO
import logging

from flask import Blueprint
from flask import g
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
import pyotp
import qrcode

from ..repository.db import get_db

logger = logging.getLogger(__name__)

bp = Blueprint("user", __name__, url_prefix="/user")


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


@bp.route("/home")
@login_required
def home():
    """Shown the users home page."""
    return render_template("user/home.html", messagesLink="")


@bp.route("/security", methods=("GET", "POST"))
@login_required
def security():
    """Display and update the users security configuration."""
    if g.user['otp_enabled']:
        # 2FA is already enabled
        secret = g.user['otp_secret']
    else:
        # Generate and store a secret for the user  
        user_id: int = session["user_id"]
        secret = pyotp.random_base32()
        db = get_db()
        error = None
        db.execute(
            "UPDATE users SET otp_enabled=?, otp_secret=? WHERE id=?",
            (1, secret, user_id),
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

    return render_template("user/security.html", qr_b64=qr_b64, secret=secret)

