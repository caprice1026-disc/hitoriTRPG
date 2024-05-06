from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config
from .models import User
from openai_service import create_thread

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATES_FOLDER)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)
    create_thread()


    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # モジュールのインポートは、循環参照を避けるためにここで行う
    from . import routes, models, auth, errors

    return app