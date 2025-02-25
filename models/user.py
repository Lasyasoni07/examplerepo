from sqlalchemy import Column, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    house_no = Column(String)
    street_name = Column(String)
    city = Column(String)
    state = Column(String)
    pincode = Column(String)
    password = Column(String)

    cart_items = relationship("Cart", back_populates="user")