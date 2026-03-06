from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    street: str
    city: str
    province: str
    phone: str

    class Config:
        from_attributes = True


class productSchema(BaseModel):
    price: float
    name: str
    description: str

    class Config:
        from_attributes = True


class cartSchema(BaseModel):
    product: str
    id: int
    amount: int

    class Config:
        from_attributes = True


#login
class LoginSchema(BaseModel):
    email: str
    password: str

    class config:
        from_attributes = True


class OrderSchema(BaseModel):
    user: int

    class Config:
        from_attributes = True
