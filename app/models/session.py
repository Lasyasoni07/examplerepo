# backend/app/models/session.py
from app import db

class Session(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Session id={self.id}>'