import os
from dotenv import load_dotenv

load_dotenv()

IS_LOCAL = os.getenv("ENV") == "development"

class Config:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    JWT_SECRET = os.getenv("JWT_SECRET")
    REDIRECT_URI = "http://localhost:8000/auth/callback"

config = Config()