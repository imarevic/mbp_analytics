import os
from flask import Flask
from app import routes

# create app
def create_app():
    # create and config the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    app.static_folder = 'static'

    # register route blueprints
    from .routes import auth, dashboard, data
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(data.bp)
    app.add_url_rule('/', endpoint='index')

    return app
