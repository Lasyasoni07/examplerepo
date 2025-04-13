from app import app, db
from app.models.event import Event
from app.models.user import User
from datetime import datetime  # ✅ Import this

with app.app_context():
    db.create_all()  # Ensures all tables (including Session) are created
    if not Event.query.first():
        events = [
            Event(
                name="Concert",
                date=datetime.strptime("2025-05-01", "%Y-%m-%d").date(),
                time=datetime.strptime("18:00", "%H:%M").time(),
                location="Main Stage",
                price=20.0,
                tickets_available=100,
                image_url="concert.jpg"
            ),
            Event(
                name="Workshop",
                date=datetime.strptime("2025-05-15", "%Y-%m-%d").date(),
                time=datetime.strptime("10:30", "%H:%M").time(),
                location="Room 101",
                price=15.0,
                tickets_available=50,
                image_url="workshop.jpg"
            )
        ]
        db.session.add_all(events)

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)

    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
