from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from services.order_service import create_order
from database.database import get_db
from fastapi.templating import Jinja2Templates
from utilities.auth_utils import get_current_user
from models.user import User

router = APIRouter(
    prefix="/order",
    tags=["Order"]
)

templates = Jinja2Templates(directory="templates")

@router.post("/checkout")
def checkout(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = create_order(db, current_user.id)
    return templates.TemplateResponse("checkout.html", {"request": request, "order_id": order.id, "message": "Order placed successfully"})
