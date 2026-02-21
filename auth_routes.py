from fastapi import APIRouter, Depends, HTTPException
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from models import User
from dependecies import get_session
from main import becrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTE, SECRET_KEY
from re import compile
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone


auth_routes = APIRouter(prefix="/auth", tags=["Auth"])


def creat_token(id):
    date_expiretation = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    dict_inf = {"sub": str(id), "expiretation": int(date_expiretation.timestamp())}
    jwt_token = jwt.encode(dict_inf, SECRET_KEY, ALGORITHM)
    return jwt_token


def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not becrypt_context.verify(password, user.password):
        return False
    else:
        return user


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

        if check2 and not check4 and len(user_schemas.phone) == 9:
            password_crypt = becrypt_context.hash(user_schemas.password)
            new_user = User(user_schemas.name, user_schemas.email, password_crypt,
                            user_schemas.street, user_schemas.city,
                            user_schemas.province, user_schemas.phone,
                            user_schemas.active, user_schemas.admin)
            session.add(new_user)
            session.commit()
            return {"message": f"Account created successfully. Email: {user_schemas.email}"}
        else:
            raise HTTPException(status_code=400, detail="Bad Request")


@auth_routes.post("/login")
async def login(login_schemas: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login_schemas.email, login_schemas.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist or invalid credentials")
    else:
        access_token = creat_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
