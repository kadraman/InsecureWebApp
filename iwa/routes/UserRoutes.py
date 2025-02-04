import base64
from io import BytesIO
import logging
import pyotp
import qrcode
from flask import Blueprint, flash, request, g, render_template, session

from iwa.utils.DbUtils import load_logged_in_user
from iwa.utils.ViewUtils import login_required

from ..repository.db import get_db

logger = logging.getLogger(__name__)

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/home")
@login_required
def home():
    """
    Show the users home page.
    """
    return render_template("user/home.html", messagesLink="")


@bp.route("/security", methods=("GET", "POST"))
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

    return render_template("user/security.html", user=g.user, qr_b64=qr_b64, secret=secret)


@bp.route("/update_security", methods=("GET", "POST"))
@login_required
def update_security():
    """
    Edit the users security details.
    """
    if request.method == "POST":
        username = session["username"]
        # TODO: implement update security
        flash('Updating security details has not yet been implemented.', 'info')

    return render_template("user/update_security.html", user=g.user)
