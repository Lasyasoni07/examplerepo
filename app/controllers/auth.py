from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app import db, mail
from app.models.user import User
from app.forms import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm
import bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
import re

auth_bp = Blueprint('auth', __name__)

# Move serializer initialization inside functions
def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

@auth_bp.route('/')
def home():
    return render_template('base.html')

@auth_bp.route('/home')
def homePage():
    return render_template('home.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash('Username already taken!')
            return render_template('signup.html', form=form)
        if User.query.filter_by(email=email).first():
            flash('Email already registered!')
            return render_template('signup.html', form=form)

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('events.event_list'))
        else:
            flash('Invalid username or password.')
    current_user = User.query.get(session.get('user_id')) if 'user_id' in session else None
    return render_template('login.html', form=form, current_user=current_user)

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Flask-Session will handle cleanup
    flash('Logged out successfully!')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user:
            serializer = get_serializer()
            token = serializer.dumps(user.email, salt='password-reset-salt')
            reset_url = url_for('auth.reset_password', token=token, _external=True)

            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f'Click this link to reset your password: {reset_url}\nThis link expires in 1 hour.'

            mail.send(msg)
            flash('A password reset link has been sent to your email.')
        else:
            flash('Email not found!')
        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    try:
        serializer = get_serializer()
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The reset link is invalid or has expired.')
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            flash('Password reset successfully! Please log in.')
            return redirect(url_for('auth.login'))
        else:
            flash('Something went wrong.')
            return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form, token=token)
