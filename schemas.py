from pydantic import BaseModel
from typing import Optional, List


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
