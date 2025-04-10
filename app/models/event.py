# backend/app/models/event.py
from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tickets_available = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)  # New field for image path

    def __repr__(self):
        return f'<Event {self.name}>'
    