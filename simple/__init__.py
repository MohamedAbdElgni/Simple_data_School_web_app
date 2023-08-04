from flask import Flask,request,url_for,Markup
# Use this in the terminal to run the app with the debugger ==> flask --app main.py --debug run
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_modals import Modal
import os 



app = Flask(__name__)
#will be hidden in the future DO NOT FORGET'00b45e9801907419b5c664e2dfd58f9c2a6a9c859195bcba223aa06150emme23'
app.config['SECRET_KEY'] = open('flaskapp.venv/.key','r').read()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app=app,db=db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = f"You have to log in to see this content "

ckeditor = CKEditor(app)
modal = Modal(app)


from simple import routes 

# mm is dd in the last sesecsecsec