from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import enum

db = SQLAlchemy()

class GameStateEnum(enum.Enum):
    PROGRESSING = '進行中'
    GAME_OVER = 'ゲームオーバー'
    GAME_CLEAR = 'ゲームクリア'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), unique=True, nullable=False)
    player = db.relationship('Player', backref='user', uselist=False)

    def set_password(self, password):
        # パスワードハッシュ生成関数のダミーです。実際には実装が必要です。
        pass

    def check_password(self, password):
        # パスワード検証関数のダミーです。実際には実装が必要です。
        return True

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
