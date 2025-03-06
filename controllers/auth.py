from flask import Blueprint, render_template, request, redirect, url_for, session
from services.user_service import UserService

auth_bp = Blueprint('auth', __name__)
user_service = UserService()

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user_service.validate_user(username, password):
            session['username'] = username
            return redirect(url_for('products.product_list'))
        return "Invalid credentials", 401
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user_service.create_user(username, password):
            return redirect(url_for('auth.login'))
        return "Username already exists", 400
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))
