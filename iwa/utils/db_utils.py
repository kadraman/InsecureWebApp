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

from venv import logger
from flask import g, session

from iwa.repository.db import get_db


def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    email = session.get("email")

    if email is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        )
        logger.debug(f"Logged in user {g.user['email']}")