import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from .routes.auth import auth_bp
    from .routes.employee import employee_bp
    from .routes.manager import manager_bp
    from .routes.training import training_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp, url_prefix="/employee")
    app.register_blueprint(manager_bp, url_prefix="/manager")
    app.register_blueprint(training_bp, url_prefix="/training")

    from .utils.seed import seed_demo_data

    with app.app_context():
        db.create_all()
        seed_demo_data()

    return app
