from app import db

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    date_uploaded = db.Column(db.DateTime)
    is_favourite = db.Column(db.Boolean)
    path = db.Column(db.String)

    def __init__(self, date_uploaded, path):
        self.date_uploaded = date_uploaded
        self.path = path

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
