from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user_model import User
from app.services.auth_service import hash_password, verify_password
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('base.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = hash_password(request.form['password'])

        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and verify_password(password, user.password):
            flash('Login successful!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@auth_bp.route('/profile')
def profile():
    # Replace with actual user session handling
    return render_template('profile.html')

@auth_bp.route('/logout')
def logout():
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
