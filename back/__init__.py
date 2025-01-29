from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_mail import Mail
from flask_jwt_extended import JWTManager


load_dotenv()
bcrypt = Bcrypt()
db = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(__name__)
    
    secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')
    db_name = os.getenv('DB_NAME') 

    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_name}"
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'aysalinos@gmail.com')

    bcrypt.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    from back.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    jwt = JWTManager(app)

    from back.controllers.todo_controller import todo_bp
    app.register_blueprint(todo_bp)
    
    return app
