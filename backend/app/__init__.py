from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../database.db'
db = SQLAlchemy(app)

from app import routes
