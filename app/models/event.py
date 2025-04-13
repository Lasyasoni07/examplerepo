from app import db
from datetime import date, time

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)  # Changed from String to Date
    time = db.Column(db.Time, nullable=False)  # Changed from String to Time
    location = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tickets_available = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
