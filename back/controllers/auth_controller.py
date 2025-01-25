from flask import Blueprint, render_template, redirect, url_for, flash
from back.services.auth_service import create_user, authenticate_user
from back.forms import RegistrationForm, LoginForm

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
    if form.validate_on_submit():
        user = authenticate_user(form.email.data, form.password.data)
        if user:
            return render_template('home.html')
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
