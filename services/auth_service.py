from authlib.integrations.starlette_client import OAuth
from config import config

oauth = OAuth()
oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    userinfo_url="https://www.googleapis.com/oauth2/v2/userinfo",
    client_kwargs={"scope": "openid email profile"},
)
