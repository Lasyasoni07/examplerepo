from app import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    event = db.relationship('Event', backref='cart_items')

    def __repr__(self):
        return f'<Cart user={self.user_id} event={self.event_id} qty={self.quantity}>'