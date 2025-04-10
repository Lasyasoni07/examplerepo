# backend/app/models/order.py
from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)  # Ensure this is present
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    event = db.relationship('Event', backref='orders')

    def __repr__(self):
        return f'<Order user_id={self.user_id} event_id={self.event_id} quantity={self.quantity}>'