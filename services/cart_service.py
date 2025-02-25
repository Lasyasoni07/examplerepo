from sqlalchemy.orm import Session
from models.cart import Cart
from models.product import Product
from schemas.cart_schema import CartItemCreate
from fastapi import HTTPException

def add_to_cart(db: Session, user_id: int, cart_item: CartItemCreate):
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.inventory < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Not enough inventory available")

    product.inventory -= cart_item.quantity

    existing_cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == cart_item.product_id).first()
    if existing_cart_item:
        existing_cart_item.quantity += cart_item.quantity
    else:
        db_cart_item = Cart(
            user_id=user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.add(db_cart_item)
    db.commit()
    
def get_cart_items(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).all()
