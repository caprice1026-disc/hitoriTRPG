from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt  # パスワードのハッシュ化に使用
from config import Config
from .models import User
from flask_jwt_extended import JWTManager

app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATES_FOLDER)
app.config.from_object(Config)
jwt = JWTManager(app)
# データベースの初期化
db = SQLAlchemy(app)

# ログイン管理の初期化
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# パスワードのハッシュ化に使用するBcryptの初期化
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# モジュールのインポートは、循環参照を避けるために最後に行う
from app import routes, models, auth, errors