from flask import Flask
from .config import Config
from .db import init_db
from .routes import albums_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    app.register_blueprint(albums_bp)

    return app
