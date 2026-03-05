from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")

#jwt
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTE = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTE"))

becrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routes import auth_routes
from order_routes import order_routes
from product_routes import product_routes
from customer_routes import customer_router

app.include_router(product_routes)
app.include_router(auth_routes)
app.include_router(customer_router)
app.include_router(order_routes)
