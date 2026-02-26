from fastapi import APIRouter, Depends, HTTPException
from schemas import productSchema
from dependecies import get_session, verify_token
from sqlalchemy.orm import Session
from models import Product, User

product_routes = APIRouter(prefix="/product", tags=["product"])


@product_routes.get("/")
async def product():
    return {"message": "Product route created successfully"}


@product_routes.post("/add_product")
async def add_product(product_schemas: productSchema, user: User = Depends(verify_token()),
                      session: Session = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")
    else:
        product = Product(product_schemas.price, product_schemas.name,
                          product_schemas.stock, product_schemas.category,
                          product_schemas.description)
        session.add(product)
        session.commit()
        return {"message": "Product added successfully"}
