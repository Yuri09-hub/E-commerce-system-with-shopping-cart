from fastapi import APIRouter, Depends, HTTPException
from schemas import UserSchema
from sqlalchemy.orm import Session
from models import User
from dependecies import get_session
from main import becrypt_context
from re import compile, findall

auth_routes = APIRouter(prefix="/auth", tags=["Auth"])


@auth_routes.get("/")
async def auth():
    return {"message": "Auth route created"}


@auth_routes.post("/create_account")
async def create_account(user_schemas: UserSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(user_schemas.email == User.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already registered")
    else:
        check = compile(".@gmail.com")
        check2 = check.findall(user_schemas.email)
        check3 = compile(r"\D")
        check4 = check3.findall(user_schemas.phone)
        if check2 and not check4:
            password_crypt = becrypt_context.hash(user_schemas.password)
            new_user = User(user_schemas.name, user_schemas.email,password_crypt,
                            user_schemas.street, user_schemas.city,
                            user_schemas.province, user_schemas.phone,
                            user_schemas.active,user_schemas.admin)
            session.add(new_user)
            session.commit()
            return {"message": "Account created successfully."}
        else:
            raise HTTPException(status_code=400, detail="Bad Request")
