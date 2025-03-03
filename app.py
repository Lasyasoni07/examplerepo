import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from models.models import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatapi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app, manage_session=True)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from controllers.auth_controller import auth as auth_blueprint
from controllers.chat_controller import chat as chat_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(chat_blueprint)

from models import models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True, use_reloader=False)
