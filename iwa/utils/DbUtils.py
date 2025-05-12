
from venv import logger
from flask import g, session

from iwa.repository.db import get_db


def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    username = session.get("username")

    if username is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        )
        logger.debug(f"Logged in user {g.user['email']}")