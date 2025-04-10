# backend/app/__init__.py
import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, 
           static_folder=os.path.abspath('../frontend/static'), 
           template_folder=os.path.abspath('../frontend/templates'))
# Configurations
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_registration.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Context processor to provide current_user
@app.context_processor
def inject_user():
    from app.models.user import User  # Import User locally to avoid circular import
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return {'current_user': user}
    return {'current_user': None}

# Register blueprints
from app.controllers import auth, events, admin
app.register_blueprint(auth.auth_bp, url_prefix='/auth')
app.register_blueprint(events.events_bp)
app.register_blueprint(admin.admin_bp, url_prefix='/admin')

with app.app_context():
    db.create_all()

# Removed: from app import routes