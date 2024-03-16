from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, bcrypt
import re

auth = Blueprint('auth', __name__)

def validate_password(password):
    """パスワードの複雑性を検証する"""
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

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.game'))
        else:
            flash('ユーザー名かパスワードが違います。', 'danger')
    return render_template('auth/login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not validate_password(password):
            flash('パスワードは8文字以上で、英大文字、英小文字、数字、記号を少なくとも1種類ずつ含む必要があります。', 'danger')
            return render_template('auth/signup.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('アカウントの作成に成功しました。', 'success')

        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html')

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.get_reset_password_token()
            # メールでトークンを送信する処理をここに実装すること。後で考える。
            flash('パスワードリセットリンクを送信しました。', 'success')
        else:
            flash('Emailが見つかりません。', 'danger')
    return render_template('auth/reset_password_request.html')

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        password = request.form.get('password')
        user = User.verify_reset_password_token(token)
        if user:
            user.set_password(password)
            db.session.commit()
            flash('パスワードはリセットされました。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('セッションに問題があります。', 'danger')
    return render_template('auth/reset_password.html')