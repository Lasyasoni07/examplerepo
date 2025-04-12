import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'eventregistrationsystem'  # Replace with a strong, unique key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///event_registration.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'aysalinos@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'rvpj kdth qjrp lgoc'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME






