from app import db
from flask_login import UserMixin

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    month_uploaded = db.Column(db.DateTime)
    path = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    sharing_token = db.Column(db.String(1000), nullable=True)
    images = db.relationship('Image', backref='user', lazy=True)
