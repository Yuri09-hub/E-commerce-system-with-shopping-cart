from fastapi import APIRouter, Depends, HTTPException
from schemas import productSchema
from dependecies import get_session, verify_token
from sqlalchemy.orm import Session
from models import Product, User

product_routes = APIRouter(prefix="/product", tags=["product"])


@product_routes.get("/")
async def product():
    return {"message": "Product route"}


@product_routes.post("/add_product")
async def add_product(product_schemas: productSchema, user: User = Depends(verify_token),
                      session: Session = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")
    else:
        product = Product(price=product_schemas.price, name=product_schemas.name,
                          stock=product_schemas.stock, description=product_schemas.description)

        session.add(product)
        session.commit()
        return {"message": "Product added successfully"}


@product_routes.get("product/list_products")
async def list_products(session: Session = Depends(get_session)):
    products = session.query(Product).all()

    return {
        "products": products
    }


@product_routes.post("product/remove_product")
async def remove_product(id_product, user: User = Depends(verify_token), session: Session = Depends(get_session)):
    product = session.query(Product).filter(Product.id == id_product).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not found.")
    elif not user.admin:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")

    session.delete(product)
    session.commit()
    return {"message": "Product removed successfully"}
