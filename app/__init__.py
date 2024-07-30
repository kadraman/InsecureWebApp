import os
import random
from flask import Flask, json, redirect, render_template, request, Response, url_for
from docx import Document
from werkzeug.utils import secure_filename

from jinja2 import Template as Jinja2_Template
from jinja2 import Environment, DictLoader

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

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initial route
    @app.route('/')
    def index():
        print("[index] Rendering home page.")
        return render_template('index.html')

    # register the database commands
    from . import db
    db.init_app(app)

    # set email subscribers file
    site_root = os.path.realpath(os.path.dirname(__file__))    
    app.config['SUBSCRIBERS_FILENAME'] = os.path.join(site_root, "static", "data", "email-db.json")

    # apply the blueprints to the app
    from . import auth
    from . import products
    from . import insecure

    app.register_blueprint(auth.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(insecure.bp)

    # initialize/reset all the product and user data
    @app.route("/init-db")
    def init_db():
        print("[init_db] Initializing database.")
        db.init_db()
        return redirect(url_for("products.index"))

    return app