"""This is the main file of the app , it contains the app configuration and the app routes
    in the future this file will be split into multiple files to make the code more readable and maintainable
"""
from flask import Flask,request,url_for,Markup
# Use this in the terminal to run the app with the debugger ==> flask --app main.py --debug run
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_modals import Modal
from flask_mail import Mail
import os 

app = Flask(__name__)
#will be hidden in the future DO NOT FORGET'00b45e9801907419b5c664e2dfd58f9c2a6a9c859195bcba223aa06150emme23'

app.config['SECRET_KEY'] = open('flaskapp.venv/app_sec.key','r').read()
print(app.config['SECRET_KEY'])
# this is the database configuration for the flask sqlalchemy ext
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# this is the ckeditor configuration for the flask ckeditor ext
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
db = SQLAlchemy(app)
migrate = Migrate(app=app,db=db)
# this is the bcrypt configuration for the flask bcrypt ext
bcrypt = Bcrypt(app)
# this is the email configuration for the flask mail ext
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = open('flaskapp.venv/mail.key','r').read()
app.config['MAIL_PASSWORD'] = open('flaskapp.venv/email_pass.key','r').read()
# this is the login configuration for the flask login ext
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = f"You have to log in to see this content "

# this is the app configuration for the flask modal ext modal , mail , ckeditor
ckeditor = CKEditor(app)
modal = Modal(app)
mail = Mail(app)

from simple import routes 