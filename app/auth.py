from flask import Blueprint, request, jsonify, render_template
from app.models import User, Role
from app import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')  
def home():
    return render_template('home.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        role_name = data.get('role', 'user')

        role = Role.query.filter_by(name=role_name).first()
        if not role:
            return jsonify({"message": "Invalid role"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already exists"}), 400

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"message": "Invalid email or password"}), 401

        access_token = create_access_token(identity={"id": user.id, "role": user.role.name})
        response = jsonify(access_token=access_token, user_role=user.role.name) 
        return response, 200
    
    
    return render_template('login.html')




