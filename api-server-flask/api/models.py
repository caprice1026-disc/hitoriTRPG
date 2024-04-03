# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime

import json

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import enum
from flask_login import UserMixin
from . import db, app, bcrypt
import jwt
import datetime


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.Text())
    jwt_auth_active = db.Column(db.Boolean())
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"User {self.username}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_email(self, new_email):
        self.email = new_email

    def update_username(self, new_username):
        self.username = new_username

    def check_jwt_auth_active(self):
        return self.jwt_auth_active

    def set_jwt_auth_active(self, set_status):
        self.jwt_auth_active = set_status

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def toDICT(self):

        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['username'] = self.username
        cls_dict['email'] = self.email

        return cls_dict

    def toJSON(self):

        return self.toDICT()


class JWTTokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jwt_token = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f"Expired Token: {self.jwt_token}"

    def save(self):
        db.session.add(self)
        db.session.commit()



class GameStateEnum(enum.Enum):
    PROGRESSING = '進行中'
    GAME_OVER = 'ゲームオーバー'
    GAME_CLEAR = 'ゲームクリア'

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
        # Tx: ここでHPとSANの値が0未満になった場合の処理を追加する。
        if self.status['HP'] <= 0:
            self.game_session.state = GameStateEnum.GAME_OVER
        elif self.status['SAN'] <= 0:
            self.game_session.state = GameStateEnum.GAME_OVER
        else:
            try:
                db.session.commit()
            except:
                db.session.rollback()
                # Tx: ここでエラーメッセージを返す処理を追加する。
    def change_conditions(self, conditions_change):
        for key, value in conditions_change['add'].items():
            self.conditions[key] = value
        for key in conditions_change['remove']:
            self.conditions.pop(key, None)
        #try exeptでエラー処理を追加  
            try:
                db.session.commit()
            except:
                db.session.rollback()
                # Tx: ここでエラーメッセージを返す処理を追加する。 
    def change_inventory(self, inventory_change):
        for item in inventory_change['add']:
            self.inventory[item['name']] = item
        for item in inventory_change['remove']:
            self.inventory.pop(item['name'], None)
        for item in inventory_change['update']:
            self.inventory[item['name']] = item
        #try exeptでエラー処理を追加
            try:
                db.session.commit()
            except:
                db.session.rollback()
                # Tx: ここでエラーメッセージを返す処理を追加する。
class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Enum(GameStateEnum), nullable=False)
    progress_log = db.Column(db.Text, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', backref='game_session', uselist=False)