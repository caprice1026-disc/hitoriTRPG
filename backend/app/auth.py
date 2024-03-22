from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, bcrypt
from flask_jwt_extended import create_access_token
import re

# URLプレフィックスに/apiを追加
auth = Blueprint('auth', __name__, url_prefix='/api')

def validate_password(password):
    """パスワードの複雑性を検証する。複雑すぎるので修正を検討"""
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[_@$]", password):
        return False
    return True

@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"error": "ユーザー名かパスワードが違います。"}), 401
    # この部分はフロントエンドを実装しつつ修正する
    return render_template('auth/login.html')

@auth.route('/signup', methods=['POST'])
def signup():
    # リクエストからJSONデータを取得
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # パスワードのバリデーション
    if not validate_password(password):
        return jsonify({"error": "パスワードは8文字以上で、英大文字、英小文字、数字、記号を少なくとも1種類ずつ含む必要があります。"}), 400

    # ユーザー名またはメールアドレスが既に存在するかチェック
    if User.query.filter_by(username=username).first() is not None or User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "ユーザー名またはメールアドレスが既に使用されています。"}), 400

    # パスワードのハッシュ化とユーザーの作成
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "アカウントの作成に成功しました。"}), 201

@auth.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.get_reset_password_token()
            # メールでトークンを送信する処理をここに実装すること。後で考える。
            return jsonify({"message": "パスワードリセットのためのリンクをメールで送信しました。"}), 200
        else:
            return jsonify({"error": "ユーザーが見つかりません。"}), 404

@auth.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    if request.method == 'POST':
        password = request.form.get('password')
        user = User.verify_reset_password_token(token)
        if user:
            user.set_password(password)
            db.session.commit()
            return jsonify({"message": "パスワードのリセットに成功しました。"}), 200
        else:
            return jsonify({"error": "トークンが無効です。"}), 400
