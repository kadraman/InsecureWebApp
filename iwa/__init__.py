import logging
import os
from flask import Flask, g, redirect, render_template, url_for, session
from flask_cors import CORS

from iwa.repository.db import get_db


logger = logging.getLogger(__name__)

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "insecurewebapp.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # set default Flask log level to INFO
    logger.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # enabled CORS on api routes
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # initial route
    @app.route('/')
    def index():
        logger.info("[index] Rendering home page.")
        return render_template('index.html')

    # route to reset the database
    @app.route("/reset-db")
    def reset_db():
        logger.info("[reset_db] Re-initializing database.")
        db.init_db()
        return redirect(url_for("products.index"))
    
    # register the database commands
    from .repository import db
    db.init_app(app)
    # create and populate the database for demo
    with app.app_context():
        db.init_db()

    # set email subscribers file
    site_root = os.path.realpath(os.path.dirname(__file__))    
    app.config['SUBSCRIBERS_FILENAME'] = os.path.join(site_root, "static", "data", "email-db.json")

    # apply the blueprints to the app
    from .routes import AuthRoutes
    from .routes import ApiRoutes
    from .routes import UserRoutes
    from .routes import ProductRoutes
    from .routes import InsecureRoutes

    app.register_blueprint(AuthRoutes.bp)
    app.register_blueprint(ApiRoutes.bp)
    app.register_blueprint(UserRoutes.bp)
    app.register_blueprint(ProductRoutes.bp)
    app.register_blueprint(InsecureRoutes.bp)

    @app.before_request
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

    return app