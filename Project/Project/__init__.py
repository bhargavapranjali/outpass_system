import os
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from Project.config import Config

app = Flask(__name__, template_folder='./templates')
app.config.from_object(Config)
app.app_context().push()

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' 
mail = Mail(app)

recognition = None
session={'account_type':None}

from Project.errors.handlers import errors
from Project.main.routes import main
from Project.admins.routes import admins
from Project.students.routes import students

app.register_blueprint(main)
app.register_blueprint(students)
app.register_blueprint(admins)
app.register_blueprint(errors)

