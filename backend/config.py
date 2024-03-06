import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # 開発環境ではsqliteを使う
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

   # フロントエンドのビルドファイルのパス
    STATIC_FOLDER = os.path.join(basedir, '../frontend/build')
    TEMPLATES_FOLDER = os.path.join(basedir, 'app/templates')