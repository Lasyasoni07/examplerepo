from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', back_populates='orders')  # Clean, no overlaps needed
    event = db.relationship('Event', backref=db.backref('event_orders', lazy=True))

    def __repr__(self):
        return f'<Order {self.id} for Event {self.event_id}>'
