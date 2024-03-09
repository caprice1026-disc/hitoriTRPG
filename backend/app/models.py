from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from . import db, app, login_manager

db = SQLAlchemy()

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
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    '''
    コンディコンディションの例
    {
    "毒": "毒の状態です。HPが徐々に減少します。",
    "麻痺": "行動できない状態です。",
    }
    '''
    inventory = db.Column(JSON, default=lambda: {})  # インベントリを保存するフィールド
    '''inventoryの例
    {
    "短剣": "攻撃力+5の武器です。",
    "回復薬": "HPを30回復します。",
    "鍵": "宝箱を開けるのに必要なアイテムです。"}
    '''
    def update_hp(self, amount):
    # amountはHPの増減量
        self.status['HP'] += amount
        # HPが0以下になった場合の処理もここに実装する
        if self.status['HP'] <= 0:
            self.status['HP'] = 0
            self.status['SAN'] = 0
            self.conditions['死亡'] = '死亡しました。'
            # ゲームオーバー処理
            self.game_session.state = GameStateEnum.GAME_OVER
            self.game_session.progress_log = 'ゲームオーバー'
            db.session.commit()
            return 'ゲームオーバー'
        return 'HPを更新しました。'
    def update_SAN(self, amount):
        self.status['SAN'] += amount
        if self.status['SAN'] <= 0:
            self.status['SAN'] = 0
            self.status['HP'] = 0
            self.conditions['狂気'] = '狂気により死亡しました。'
            self.game_session.state = GameStateEnum.GAME_OVER
            self.game_session.progress_log = 'ゲームオーバー'
            db.session.commit()
            return 'ゲームオーバー'
        return 'SANを更新しました。'
    def add_item_to_inventory(self, item_name, item_description):
        # item_nameはアイテムの名前、item_descriptionはアイテムの説明
        self.inventory[item_name] = item_description
        db.session.commit()
        return 'アイテムを追加しました。'
    # アイテム削除の関数。使用の際もここを参照する。
    def remove_item_from_inventory(self, item_name):
        # item_nameはアイテムの名前
        del self.inventory[item_name]
        db.session.commit()
        return 'アイテムを削除しました。'
    def change_status(self, status_name, amount):
        # status_nameはステータスの名前、amountは増減量
        self.status[status_name] += amount
        db.session.commit()
        return 'ステータスを変更しました。'
    def add_conditions(self, condition_name, condition_description):
        # condition_nameは状態異常の名前、condition_descriptionは状態異常の説明
        self.conditions[condition_name] = condition_description
        db.session.commit()
        return '状態異常を追加しました。'
    def remove_conditions(self, condition_name):
        # condition_nameは状態異常の名前
        del self.conditions[condition_name]
        db.session.commit()
        return '状態異常を削除しました。'
    world_id = db.Column(db.Integer, db.ForeignKey('world_setting.id'), nullable=True)
    world = db.relationship('WorldSetting', backref='players', uselist=False)

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Enum(GameStateEnum), nullable=False)
    # ここはnullの可能性があるので修正するかも
    progress_log = db.Column(db.Text, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', backref='game_session', uselist=False)

# 必要に応じて、パスワードのハッシュ化と検証のための実際の関数を実装

# データベース初期化のための関数や、プレイヤーのHPとSANを更新するためのロジックは、
# このファイル外で定義する必要があります。それらはアプリケーションのビジネスロジックの一部として、
# モデルのインスタンスが作成または更新される際に適切に呼び出す。
