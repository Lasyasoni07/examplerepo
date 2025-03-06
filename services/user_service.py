from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def create_user(self, username, password):
        if User.query.filter_by(username=username).first():
            return False
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return True

    def validate_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return True
        return False
