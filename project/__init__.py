import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login = LoginManager()


def create_app(script_info=None):

    app = Flask(__name__)

    # When given the direct file path i.e., >> "project.config.DevelopmentConfig"
    # it doesn't give UserWarning and DeprecationWaring, but when asked to derive from
    # .flaskenv, it gives the warning

    app_settings = os.environ.get('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app=app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login.init_app(app)

    from project.app.models import User
    from project.app.users import users_blueprint
    app.register_blueprint(users_blueprint)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
