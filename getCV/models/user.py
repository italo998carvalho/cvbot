from getCV import db
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cv = db.Column(JSON)

    def __init__(self, cv):
        self.cv = cv