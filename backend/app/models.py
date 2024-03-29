from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import enum
from flask_login import UserMixin
from . import db, app, bcrypt
import jwt
import datetime

class GameStateEnum(enum.Enum):
    PROGRESSING = '進行中'
    GAME_OVER = 'ゲームオーバー'
    GAME_CLEAR = 'ゲームクリア'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), unique=True, nullable=False)
    player = db.relationship('Player', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': datetime.datetime.now() + datetime.timedelta(seconds=expires_in)},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class WorldSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(100), nullable=False)
    stage = db.Column(db.String(100), nullable=False)
    chaos_level = db.Column(db.Integer, nullable=False)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    job = db.Column(db.String(100), nullable=False)
    status = db.Column(JSON, default=lambda: {
        "STR": 0,
        "DEX": 0, 
        "INT": 0, 
        "AGI": 0, 
        "LUCK": 0,
        "HP": 50, 
        "SAN": 100
    })
    conditions = db.Column(JSON, default=lambda: {})  
    inventory = db.Column(JSON, default=lambda: {})  
    world_id = db.Column(db.Integer, db.ForeignKey('world_setting.id'), nullable=True)
    world = db.relationship('WorldSetting', backref='players', uselist=False)
    def change_status(self, status_change):
        for key, value in status_change.items():
            self.status[key] += value
        # Tx: ここでHPとSANの値が0未満になった場合の処理を追加する
        if self.status['HP'] <= 0:
            self.game_session.state = GameStateEnum.GAME_OVER
        elif self.status['SAN'] <= 0:
            self.game_session.state = GameStateEnum.GAME_OVER
        #try exeptでエラー処理を追加
        db.session.commit()
    def change_conditions(self, conditions_change):
        for key, value in conditions_change['add'].items():
            self.conditions[key] = value
        for key in conditions_change['remove']:
            self.conditions.pop(key, None)
        #try exeptでエラー処理を追加   
        db.session.commit
    def change_inventory(self, inventory_change):
        for item in inventory_change['add']:
            self.inventory[item['name']] = item
        for item in inventory_change['remove']:
            self.inventory.pop(item['name'], None)
        for item in inventory_change['update']:
            self.inventory[item['name']] = item
        #try exeptでエラー処理を追加
        db.session.commit
class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Enum(GameStateEnum), nullable=False)
    progress_log = db.Column(db.Text, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', backref='game_session', uselist=False)

# データベース初期化のための関数や、プレイヤーのHPとSANを更新するためのロジックは、
# このファイル外で定義する必要がある。それらはアプリケーションのビジネスロジックの一部として、
# モデルのインスタンスが作成または更新される際に適切に呼び出す。

