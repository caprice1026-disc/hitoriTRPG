from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
import jwt
import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
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
        user = User(username=username, email=email)
        user.set_password(password)
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
            flash('Password has been reset', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid or expired token', 'danger')
    return render_template('auth/reset_password.html')