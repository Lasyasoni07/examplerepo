from pydantic import BaseModel, EmailStr, validator

class UserBase(BaseModel):
    username: str
    phone_number: str
    email: EmailStr
    house_no: str
    street_name: str
    city: str
    state: str
    pincode: str

class UserCreate(UserBase):
    password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserLogin(BaseModel):
    username: str
    password: str

class ShowUser(UserBase):
    id: int

    class Config:
        orm_mode = True
