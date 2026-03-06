from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from models import User
from dependecies import get_session, verify_token, validate_province
from main import becrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTE, SECRET_KEY
from re import compile
from jose import jwt
from datetime import timedelta, datetime, timezone

auth_routes = APIRouter(prefix="/auth", tags=["Auth"])


def validate_email(email):
    check = compile(".@gmail.com")
    check2 = check.findall(email)
    if check2:
        return True
    else:
        return False


def validate_number(phone):
    check3 = compile(r"\D")
    check4 = check3.findall(phone)
    if not check4 and len(phone) == 9:
        return True
    else:
        return False


def creat_token(id, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)):
    date_expiretation = datetime.now(timezone.utc) + duration_token
    dict_inf = {"sub": str(id), "exp": int(date_expiretation.timestamp())}
    jwt_token = jwt.encode(dict_inf, SECRET_KEY, ALGORITHM)
    return jwt_token


def authenticate_user(email, password, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not becrypt_context.verify(password, user.password):
        return False
    else:
        return user


@auth_routes.post("/create_account")
async def create_account(user_schemas: UserSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(user_schemas.email == User.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already registered")

    if not validate_email(user_schemas.email):
        raise HTTPException(status_code=400, detail="Email is not valid")
    elif not validate_number(user_schemas.phone):
        raise HTTPException(status_code=400, detail="Phone number is not valid")
    elif not validate_province(user_schemas.province.title()):
        raise HTTPException(status_code=400, detail="Province is not valid")

    password_crypt = becrypt_context.hash(user_schemas.password)
    new_user = User(user_schemas.name.title(), user_schemas.email, password_crypt,
                    user_schemas.street.title(), user_schemas.city.title(),
                    user_schemas.province.title(), user_schemas.phone)
    session.add(new_user)
    session.flush()

    user = session.query(User).filter(User.id == 1).first()
    if user:
        user.admin = True
    session.commit()
    return {"message": f"Account created successfully."}


@auth_routes.post("/login")
async def login(login_schemas: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login_schemas.email, login_schemas.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist or invalid credentials")
    else:
        access_token = creat_token(user.id)
        refresh_token = creat_token(user.id, duration_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }


@auth_routes.post("/login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist or invalid credentials")
    else:
        access_token = creat_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


@auth_routes.get("/refresh")
async def user_refresh_token(user: User = Depends(verify_token)):
    access_token = creat_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
