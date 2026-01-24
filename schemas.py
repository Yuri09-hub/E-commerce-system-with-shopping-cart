from pydantic import BaseModel
from typing import Optional, List


class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    street: Optional[str]
    city: str
    province: str
    phone: Optional[int]
    active: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True
