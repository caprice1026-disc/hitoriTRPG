from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from .models import User

app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATES_FOLDER)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes, models, auth, errors
