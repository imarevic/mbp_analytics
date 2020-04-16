import os
from flask import Flask
from app import routes

# create app
def create_app():
    # create and config the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)

    # register route blueprints
    from .routes import login, dashboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)

    return app
