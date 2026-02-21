from fastapi import FastAPI
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
becrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from auth_routes import auth_routes
from order_routes import order_routes

app.include_router(auth_routes)
app.include_router(order_routes)
