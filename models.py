from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import UserMixin

from datetime import datetime
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # suppresses a warning message
app.config['WTF_CSRF_ENABLED'] = False # suppress Flask-wtf cross-site registry forgery protection
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    gifts = db.relationship('Gift', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Gift(db.Model):
    __tablename__ = "gift"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)
    # holiday = db.relationship('Gift', backref='gift', lazy=True)

    def __repr__(self):
        return f"Gift( '{self.title}', '{self.date_posted}')"


class Holidays(db.Model):
    __tablename__ = "holiday"

    id = db.Column(db.Integer, primary_key=True)
    gift_id = db.Column(db.Integer, db.ForeignKey('gift.id'), nullable=False)
    holiday = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"Holiday( '{self.Holiday}'"

db.drop_all()
db.create_all()