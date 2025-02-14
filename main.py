from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from controllers.auth_controller import router as auth_router
from controllers.user_controller import router as user_router
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

IS_LOCAL = os.getenv("ENV") == "development"

app.add_middleware(
    SessionMiddleware,
    secret_key="your_super_secret_key",
    session_cookie="fastapi_session",
    same_site="lax", 
    https_only=False, 
    max_age=86400, 
)

app.include_router(auth_router, prefix="")
app.include_router(user_router, prefix="")

@app.get("/", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/test_session")
async def test_session(request: Request):
    request.session["test"] = "Session Works!"
    return {"message": "Session set!"}
