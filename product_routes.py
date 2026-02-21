from fastapi import APIRouter, Depends, HTTPException
from schemas import  productSchema,LoginSchema
from dependecies import get_session
from sqlalchemy.orm import Session
from auth_routes import authenticate_user
from models import Product

product_routes = APIRouter(prefix="/product", tags=["product"])


@product_routes.get("/")
async def product():
    return {"message": "Product route created successfully"}


@product_routes.post("/add_product")
async def add_product(login_schemas: LoginSchema, product_schemas: productSchema,
                      session: Session = Depends(get_session)):
    user = authenticate_user(login_schemas.email, login_schemas.password, session)
    if not user.admin:
        raise HTTPException(status_code=400, detail="You do not have permission to make this.")
    else:
        product = Product(product_schemas.price, product_schemas.name,
                          product_schemas.stock, product_schemas.category,
                          product_schemas.description)
        session.add(product)
        session.commit()
        return {"message": "Product added successfully"}
