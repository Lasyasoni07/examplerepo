from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from services.product_service import get_products, create_product
from schemas.product_schema import ProductCreate
from database.database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from utilities.auth_utils import get_current_user
from models.user import User

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/")
def list_products(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = get_products(db)
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@router.post("/add")
def add_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    inventory: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = ProductCreate(
        name=name,
        description=description,
        price=price,
        category=category,
        inventory=inventory
    )
    create_product(db, product)
    return RedirectResponse(url="/products", status_code=HTTP_303_SEE_OTHER)
