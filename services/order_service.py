from sqlalchemy.orm import Session
from models.order import Order
from models.cart import Cart
from models.product import Product
from fastapi import HTTPException

def create_order(db: Session, user_id: int):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    order = Order(user_id=user_id, total_amount=total_amount)
    db.add(order)

    for item in cart_items:
        db.delete(item)

    db.commit()
    db.refresh(order)
    return order
