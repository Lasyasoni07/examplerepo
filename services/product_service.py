from sqlalchemy.orm import Session
from models.product import Product
from schemas.product_schema import ProductCreate

def get_products(db: Session):
    return db.query(Product).all()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_inventory(db: Session, product_id: int, quantity: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    product.inventory -= quantity
    db.commit()
    return product

def decrease_inventory(db: Session, product_id: int, quantity: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    product.inventory -= quantity
    db.commit()
    return product
