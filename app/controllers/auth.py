from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app import db, mail
from app.models.user import User
from app.forms import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm, ContactForm
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from authlib.integrations.flask_client import OAuthError
from app.models.contact_query import ContactQuery

auth_bp = Blueprint('auth', __name__)

def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

@auth_bp.route('/')
def home():
    return render_template('home.html')

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
        confirm_password = form.confirm_password.data

        if User.query.filter_by(username=username).first():
            flash('Username already taken!', 'danger')
            return render_template('signup.html', form=form)
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return render_template('signup.html', form=form)

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html', form=form)

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.capitalize()}: {error}", 'danger')

    return render_template('signup.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('events.event_list'))
        else:
            flash('Invalid username or password.', 'danger')
    current_user = User.query.get(session.get('user_id')) if 'user_id' in session else None
    return render_template('login.html', form=form, current_user=current_user)

@auth_bp.route('/google/login')
def google_login():
    redirect_uri = url_for('auth.google_auth', _external=True)
    return current_app.extensions['authlib.integrations.flask_client'].google.authorize_redirect(redirect_uri)

@auth_bp.route('/auth/google')
def google_auth():
    try:
        token = current_app.extensions['authlib.integrations.flask_client'].google.authorize_access_token()
        user_info = current_app.extensions['authlib.integrations.flask_client'].google.parse_id_token(token, nonce=None)
        email = user_info['email']
        name = user_info.get('name', '')
        
        user = User.query.filter_by(email=email).first()
        if not user:
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1
            user = User(username=username, email=email)
            user.set_password(None)
            db.session.add(user)
            db.session.commit()
            flash('Signed up with Google! Welcome!', 'success')
        else:
            flash('Logged in with Google!', 'success')
        
        session['user_id'] = user.id
        return redirect(url_for('events.event_list'))
    
    except OAuthError as e:
        flash(f'Google authentication failed: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
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
            flash('A password reset link has been sent to your email.', 'success')
        else:
            flash('Email not found!', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    try:
        serializer = get_serializer()
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            flash('Password reset successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Something went wrong.', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form, token=token)

@auth_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        query = ContactQuery(
            username=form.username.data,
            email=form.email.data,
            message=form.message.data
        )
        try:
            db.session.add(query)
            db.session.commit()
            flash('Your query has been submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Something went wrong. Please try again.', 'danger')
        return redirect(url_for('auth.contact')) 
    return render_template('contact.html', form=form)