from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.orm import Session
from services.cart_service import add_to_cart, get_cart_items
from schemas.cart_schema import CartItemCreate
from database.database import get_db
from models.user import User
from models.cart import Cart
from models.product import Product
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from utilities.auth_utils import get_current_user
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

templates = Jinja2Templates(directory="templates")

@router.post("/add")
def add_item_to_cart(
    request: Request,
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_item_data = CartItemCreate(
        product_id=product_id,
        quantity=quantity
    )
    add_to_cart(db, current_user.id, cart_item_data)
    return RedirectResponse(url="/cart/items", status_code=HTTP_303_SEE_OTHER)

@router.get("/items")
def view_cart(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_items = get_cart_items(db, current_user.id)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart_items": cart_items,
        "total_amount": total_amount
    })

@router.post("/remove")
def remove_item_from_cart(
    request: Request,
    cart_item_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_item = db.query(Cart).filter(Cart.id == cart_item_id, Cart.user_id == current_user.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    # Restock the inventory
    cart_item.product.inventory += cart_item.quantity

    # Remove from cart
    db.delete(cart_item)
    db.commit()
    return RedirectResponse(url="/cart/items", status_code=HTTP_303_SEE_OTHER)
