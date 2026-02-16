from fastapi import APIRouter, Depends, HTTPException
from schemas import UserSchema
from sqlalchemy.orm import Session
from models import User
from dependecies import get_session
from main import becrypt_context
from re import compile

auth_routes = APIRouter(prefix="/auth", tags=["Auth"])


@auth_routes.get("/")
async def auth():
    return {"message": "Auth route created"}


@auth_routes.post("/create_account")
async def create_account(user_schemas: UserSchema,session: Session = Depends(get_session)):
    user = session.query(User).filter(user_schemas.email == User.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already registered")
    else:
        encrypted_password = becrypt_context.hash(user_schemas.password)

        new_user = User(user_schemas.name, user_schemas.email, encrypted_password,
                        user_schemas.street,user_schemas.city,
                        user_schemas.province,user_schemas.phone,
                        user_schemas.admin,user_schemas.active)
        session.add(new_user)
        session.commit()
