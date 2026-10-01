from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config


db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        if hasattr(test_config, "items"):
            app.config.update(test_config)
        else:
            app.config.from_object(test_config)

    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = app.config["MAX_UPLOAD_MB"] * 1024 * 1024

    for directory in (app.config["BOOKS_DIR"], app.config["COVERS_DIR"], app.config["DATA_DIR"]):
        Path(directory).mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    from .routes.books import books_bp
    from .routes.main import main_bp
    from .routes.opds import opds_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(opds_bp)

    with app.app_context():
        db.create_all()
        from .services.library import LibraryScanner

        LibraryScanner(app).scan()

    return app
