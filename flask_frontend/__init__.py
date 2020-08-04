import os
from flask import Flask
from flask_frontend.app_handlers import register_app_handlers
from errors.bp import jwt, register_error_handlers
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    jwt.init_app(app)
    with app.app_context():

        from news.bp import news_bp
        from users.bp import users_bp
        from errors.bp import errors_bp

        app.register_blueprint(news_bp)
        app.register_blueprint(users_bp)
        app.register_blueprint(errors_bp)

    register_error_handlers(app)
    register_app_handlers(app)

    return app
