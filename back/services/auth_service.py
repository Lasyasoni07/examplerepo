from back.models.user_model import User
from back import db, bcrypt
from flask import flash

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.check_password_hash(hashed_password, password)

def create_user(first_name, last_name, email, password):
    if User.query.filter_by(email=email).first():
        flash('Email is already registered.', 'error')
        return None

    hashed_password = hash_password(password)
    new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash('Signup successful! Please log in.', 'success')
    return new_user

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and verify_password(password, user.password):
        flash('Login successful!', 'success')
        return user
    else:
        flash('Invalid email or password.', 'error')
        return None
