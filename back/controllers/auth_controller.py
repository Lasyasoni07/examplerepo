import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from back.models.user_model import User
from back.services.auth_service import hash_password, verify_password
from back import db

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    return len(password) >= 8 and re.search(r"[A-Za-z]", password) and re.search(r"\d", password)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(first_name) <= 1:
            flash('First name must be more than 1 character.', 'error')
            return redirect(url_for('auth.sign_up'))

        if len(last_name) <= 1:
            flash('Last name must be more than 1 character.', 'error')
            return redirect(url_for('auth.sign_up'))

        if not first_name or not last_name or not email or not password1 or not password2:
            flash('All fields are required.', 'error')
            return render_template('signup.html')
        
        if not is_valid_email(email):
            flash('Invalid email address.', 'error')
            return render_template('signup.html')
        
        if not is_valid_password(password1):
            flash('Password must be at least 8 characters long, contain letters, numbers, and a special character.', 'error')
            return render_template('signup.html')

        if password1 != password2:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')

        if User.query.filter_by(email=email).first():
            flash('Email is already registered.', 'error')
            return render_template('signup.html')

        hashed_password = hash_password(password1)
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Both email and password are required.', 'error')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()

        if user and verify_password(password, user.password):
            flash('Login successful!', 'success')
            return render_template('home.html')
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')

    return render_template('login.html')


@auth_bp.route('/')
def home():
    return render_template('base.html')

@auth_bp.route('/view-profile')
def view_profile():

    return render_template('viewprofile.html')

@auth_bp.route('/logout')
def logout():
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
