from pydantic import BaseModel

class OrderBase(BaseModel):
    user_id: int
    total_amount: float

class ShowOrder(OrderBase):
    id: int

    class Config:
        orm_mode = True
