import logging
import os
from flask import Flask, g, redirect, render_template, url_for, session
from flask_session import Session
from flask_cors import CORS

#from iwa.openai import OpenAI
from iwa.repository.db import get_db


logger = logging.getLogger(__name__)
#openai_extension = OpenAI()

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "insecurewebapp.sqlite"),
        # session type
        SESSION_TYPE="filesystem",
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

    # OpenAI configuration for Agent
    #app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    #openai_extension.init_app(app)

    Session(app)
  
    # 404 error handler
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    # 500 error handler
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    # register the database commands
    from .repository import db
    db.init_app(app)
    # create and populate the database for demo
    with app.app_context():
        db.init_db()

    # set email subscribers file
    site_root = os.path.realpath(os.path.dirname(__file__))    
    app.config['SUBSCRIBERS_FILENAME'] = os.path.join(site_root, "static", "data", "email-db.json")

    # register blueprints

    from iwa.main.routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    from iwa.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from iwa.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from iwa.users.routes import users_bp
    app.register_blueprint(users_bp, url_prefix='/user')

    from iwa.products.routes import products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    #from iwa.agent.routes import agent_bp
    #app.register_blueprint(agent_bp)

    from iwa.insecure.routes import insecure_bp
    app.register_blueprint(insecure_bp, url_prefix='/insecure')

    return app