from flask import Flask

from web.config import Config
from web.routes import main_bp


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    app.config["UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)
    app.register_blueprint(main_bp)

    return app
