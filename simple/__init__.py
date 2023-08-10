"""This is the main file of the app , it contains the app configuration and the app routes
    in the future this file will be split into multiple files to make the code more readable and maintainable
"""
import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_modals import Modal
from flask_mail import Mail
from flask import Flask
from simple.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate(db=db)
ckeditor = CKEditor()
modal = Modal()
mail = Mail()
login_manager = LoginManager()

login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
login_manager.login_message = "You have to log in to see this content"

def create_app(config_class=Config):
    """This function is used to create the app instance , it is used by the flask shell to create the app instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    modal.init_app(app)
    mail.init_app(app)
    
    from simple.main.routes import main # pylint: disable=wrong-import-position
    from simple.users.routes import users # pylint: disable=wrong-import-position
    from simple.lessons.routes import lessons # pylint: disable=wrong-import-position
    from simple.courses.routes import courses_bp # pylint: disable=wrong-import-position
    
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(lessons)
    app.register_blueprint(courses_bp)
    
    return app