from pydantic import BaseModel
from schemas.product_schema import ShowProduct

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class ShowCartItem(BaseModel):
    id: int
    product: ShowProduct
    quantity: int

    class Config:
        orm_mode = True
