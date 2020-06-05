from app import db

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    date_uploaded = db.Column(db.DateTime)
    is_favourite = db.Column(db.Boolean)
    path = db.Column(db.String)

    def __init__(self, date_uploaded, favourite, path):
        self.date_uploaded = date_uploaded
        self.favourite = favourite
        self.path = path
