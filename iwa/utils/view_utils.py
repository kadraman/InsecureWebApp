
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
import functools
import logging
import pickle

from flask import g, make_response, redirect, render_template, session, url_for


logger = logging.getLogger(__name__)


class usr:
    def __init__(self, email, password):
        self.email = email
        self.password = password


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['email'] is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def gen_login_cookie(cookie_name, template):
    email = session["email"]
    password = session["password"]
    logger.debug(f"Creating {cookie_name} cookie for {email}:{password}")
    u1 = usr(email, password)
    ser = pickle.dumps(u1)
    b64 = base64.b64encode(ser)
    res = make_response(render_template(template))
    res.set_cookie(cookie_name, b64, 60*60*24*15)
    return res