from typing import Any

from flask import Flask

from .models import db


def create_app(config_class: Any = "config.Config") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        from . import routes

        app.register_blueprint(routes.bp)
        db.create_all()

    return app
