from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')
    db_name = os.getenv('DB_NAME') 

    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_name}"

    bcrypt.init_app(app)
    db.init_app(app)

    from back.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)
    
    return app
