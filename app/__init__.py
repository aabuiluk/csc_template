from flask import Flask

from app.deploy import deploy_bp
from app.routes import main_bp
from app.students import load_for_web


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(deploy_bp)
    load_for_web(app)
    return app
