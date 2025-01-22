import logging
import os
import random
from flask import Flask, json, redirect, render_template, request, Response, url_for
from flask_cors import CORS
from docx import Document
from werkzeug.utils import secure_filename

from jinja2 import Template as Jinja2_Template
from jinja2 import Environment, DictLoader

logger = logging.getLogger(__name__)

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "fortifydemoapp.sqlite"),
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
    
    # user dahboard
    @app.route('/dashboard')
    def dashboard():
        logger.info("[dashboard] Rendering user dashboard.")
        return render_template('dashboard.html', messagesLink="")

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
    from .routes import ProductRoutes
    from .routes import InsecureRoutes

    app.register_blueprint(AuthRoutes.bp)
    app.register_blueprint(ApiRoutes.bp)
    app.register_blueprint(ProductRoutes.bp)
    app.register_blueprint(InsecureRoutes.bp)

    return app