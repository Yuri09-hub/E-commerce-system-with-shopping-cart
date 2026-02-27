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
    active: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class productSchema(BaseModel):
    price: float
    name: str
    description: str
    stock: int
    category: str

    class Config:
        from_attributes = True


class cartSchema(BaseModel):
    product: str
    amount: int

    class Config:
        from_attributes = True


#login
class LoginSchema(BaseModel):
    email: str
    password: str

    class config:
        from_attributes = True


#cart
class CartSchema(BaseModel):
    product: str
    amount: int
    unit_price: float

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    user: int
    payment: str

    class Config:
        from_attributes = True
