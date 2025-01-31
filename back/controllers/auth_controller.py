from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from back.services.auth_service import create_user, authenticate_user
from back.validations.forms import RegistrationForm, LoginForm
from flask import request, current_app
from back.validations.forms import RequestResetForm, ResetPasswordForm
from back.services.auth_service import generate_reset_token, verify_reset_token, hash_password
from flask_mail import Message
from back import mail, db
from back.models.user_model import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, JWTManager


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 != password2:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html', form=form)

        user = create_user(first_name, last_name, email, password1)
        if user:
            return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)
    
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = authenticate_user(email, password)
        if user:
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    return render_template('login.html', form=form)


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

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_reset_token(email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            send_reset_email(user.email, reset_url)
            flash('Password reset link has been sent to your email.', 'info')
        else:
            flash('Email not found.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('request_reset.html', form=form)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('The reset link is invalid or has expired.', 'error')
        return redirect(url_for('auth.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hash_password(form.password1.data)
            db.session.commit()
            flash('Your password has been reset successfully!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)

def send_reset_email(to_email, reset_url):
    msg = Message('Password Reset Request',
                  recipients=[to_email],
                  body=f"Please click the link to reset your password: {reset_url}")
    mail.send(msg)

@auth_bp.route('/verify-token', methods=['POST'])
@jwt_required()
def verify_token():
    return jsonify({'valid': True}), 200