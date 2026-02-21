from fastapi import APIRouter, Depends, HTTPException
from schemas import UserSchema, productSchema
from dependecies import get_session
from sqlalchemy.orm import Session


product_routes = APIRouter(prefix="/product", tags=["product"])


@product_routes.get("/")
async def product():
    return {"message": "Product route created successfully"}

#@product_routes.post("/add_product")
#async def add_product(user_schemas:UserSchema,product_schemas:productSchema,
#                      session: Session = Depends(get_session)):


