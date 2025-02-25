from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    inventory: int

class ProductCreate(ProductBase):
    pass

class ShowProduct(ProductBase):
    id: int

    class Config:
        orm_mode = True
