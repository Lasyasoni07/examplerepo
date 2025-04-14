import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from config import Config

app = Flask(__name__, 
            static_folder=os.path.abspath('../frontend/static'), 
            template_folder=os.path.abspath('../frontend/templates'))

# Load configurations
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

# Flask-Session setup
app.config['SESSION_SQLALCHEMY'] = db
sess = Session(app)

# OAuth for Google
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from app.models.user import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.context_processor
def inject_user():
    from app.models.user import User
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return {'current_user': user}
    return {'current_user': None}

# Import models for migrations
from app.models.user import User
from app.models.event import Event
from app.models.cart import Cart
from app.models.order import Order
from app.models.contact_query import ContactQuery

# Register blueprints
from app.controllers import auth, events, admin
app.register_blueprint(auth.auth_bp, url_prefix='/')
app.register_blueprint(events.events_bp)
app.register_blueprint(admin.admin_bp, url_prefix='/admin')