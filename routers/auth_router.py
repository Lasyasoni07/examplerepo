from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from services.auth_service import create_user, authenticate_user
from schemas.user_schema import UserCreate
from database.database import get_db
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER
from starlette.middleware.sessions import SessionMiddleware

router = APIRouter(
    tags=["Authentication"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/register")
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    house_no: str = Form(...),
    street_name: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    pincode: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = UserCreate(
        username=username,
        phone_number=phone_number,
        email=email,
        house_no=house_no,
        street_name=street_name,
        city=city,
        state=state,
        pincode=pincode,
        password=password,
        confirm_password=confirm_password
    )
    create_user(db, user)
    return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)

@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if user:
        response = RedirectResponse(url="/products", status_code=HTTP_303_SEE_OTHER)
        request.session["user_id"] = user.id
        return response
    return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials"})

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)