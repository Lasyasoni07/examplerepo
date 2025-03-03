import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_login import LoginManager
from models.models import db
from socketio_instance import socketio

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatapi.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    socketio.init_app(app, manage_session=False)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import models
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    from flask_login import current_user
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    from controllers.auth_controller import auth as auth_blueprint
    from controllers.chat_controller import chat as chat_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(chat_blueprint)

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
