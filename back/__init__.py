from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    bcrypt.init_app(app)
    db.init_app(app)

    from back.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)
    

    return app



 
