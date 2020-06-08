from app import db
from flask_login import UserMixin

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    date_uploaded = db.Column(db.DateTime)
    is_favourite = db.Column(db.Boolean)
    path = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __init__(self, date_uploaded, path, user_id):
        self.date_uploaded = date_uploaded
        self.path = path
        self.is_favourite = False
        self.user_id = user_id

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    images = db.relationship('Image', backref='user', lazy=True)
