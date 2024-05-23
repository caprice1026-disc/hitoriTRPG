from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()

class PlayerStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', back_populates='status')
    strength = db.Column(db.Integer, default=0)
    dexterity = db.Column(db.Integer, default=0)
    intelligence = db.Column(db.Integer, default=0)
    agility = db.Column(db.Integer, default=0)
    luck = db.Column(db.Integer, default=0)
    hp = db.Column(db.Integer, default=50)
    sanity = db.Column(db.Integer, default=100)

class PlayerCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', back_populates='conditions')
    condition_type = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)

class PlayerInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', back_populates='inventory')
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    job = db.Column(db.String(100), nullable=False)
    status = db.relationship('PlayerStatus', back_populates='player', uselist=False, lazy='joined')
    conditions = db.relationship('PlayerCondition', back_populates='player', lazy='dynamic')
    inventory = db.relationship('PlayerInventory', back_populates='player', lazy='dynamic')

    def update_status(self, changes):
        try:
            for key, value in changes.items():
                if hasattr(self.status, key):
                    setattr(self.status, key, value)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to update Player status: {str(e)}")

    def add_condition(self, condition_type, value):
        try:
            new_condition = PlayerCondition(condition_type=condition_type, value=value, player_id=self.id)
            db.session.add(new_condition)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to add Player condition: {str(e)}")

    def update_inventory(self, item_name, quantity):
        try:
            item = PlayerInventory.query.filter_by(player_id=self.id, item_name=item_name).first()
            if item:
                item.quantity += quantity
            else:
                new_item = PlayerInventory(player_id=self.id, item_name=item_name, quantity=quantity)
                db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to update inventory: {str(e)}")

'''ワールドのクラスを定義する'''
class World(db.model):
    id = db.Column(db.Integer, primary_key=True)
    

# データベース初期化のための関数や、プレイヤーのHPとSANを更新するためのロジックは、
# このファイル外で定義する必要がある。それらはアプリケーションのビジネスロジックの一部として、
# モデルのインスタンスが作成または更新される際に適切に呼び出す。

