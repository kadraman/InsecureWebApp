
import base64
import functools
import logging
import pickle

from flask import g, make_response, redirect, render_template, session, url_for

logger = logging.getLogger(__name__)

class usr:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def gen_login_cookie(cookie_name, template):
    username = session["username"]
    password = session["password"]
    logger.info(f"Creating {cookie_name} cookie for {username}:{password}")
    u1 = usr(username, password)
    ser = pickle.dumps(u1)
    b64 = base64.b64encode(ser)
    res = make_response(render_template(template))
    res.set_cookie(cookie_name, b64, 60*60*24*15)
    return res