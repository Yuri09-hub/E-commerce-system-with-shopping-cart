from fastapi import APIRouter, Depends, HTTPException
from schemas import productSchema
from dependecies import get_session, verify_token
from sqlalchemy.orm import Session
from models import Product, User, product_entry, product_output
from datetime import datetime, timezone

product_routes = APIRouter(prefix="/product", tags=["Product"])


@product_routes.post("/add_product")
async def add_product(amount, product_schemas: productSchema, user: User = Depends(verify_token),
                      session: Session = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")

    product = Product(price=product_schemas.price, name=product_schemas.name,
                      description=product_schemas.description)
    session.add(product)
    session.flush()

    new_entry = product_entry(product_id=product.id, amount=amount, date=datetime.now(timezone.utc))

    session.add(new_entry)
    session.commit()
    return {"message": "Product added successfully"}


@product_routes.post("/update_product")
async def update_product(id: int, product_schemas: productSchema, user: User = Depends(verify_token),
                         session: Session = Depends(get_session)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")
    find_product = session.query(Product).filter(Product.id == id).first()
    if not find_product:
        raise HTTPException(status_code=400, detail="Product not found.")

    find_product.name = product_schemas.name
    find_product.price = product_schemas.price
    find_product.description = product_schemas.description
    session.commit()
    return {"message": "Product updated successfully"}


@product_routes.get("product/list_products")
async def list_products(session: Session = Depends(get_session)):
    products = session.query(Product).limit(10).offset(0)

    return {
        "products": products
    }


@product_routes.post("product/add_stock")
async def add_stock(id_product, amount, user: User = Depends(verify_token),
                    session: Session = Depends(get_session)):
    find_product = session.query(Product).filter(Product.id == id_product).first()

    if not find_product:
        raise HTTPException(status_code=400, detail="Product not found.")
    elif not user.admin:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")

    entry = product_entry(product=find_product.id, amount=amount, date=datetime.now(timezone.utc))
    session.add(entry)
    session.commit()
    return {"message": "Product added successfully"}


@product_routes.get("product/search_product")
async def search_product(id_product, session: Session = Depends(get_session)):
    find_product = session.query(Product).filter(Product.id == id_product).first()
    if not find_product:
        raise HTTPException(status_code=400, detail="Product not found.")
    return {"product": find_product}


@product_routes.post("product/delete_product")
async def delete_product(id_product, user: User = Depends(verify_token), session: Session = Depends(get_session)):
    product = session.query(Product).filter(Product.id == id_product).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not found.")
    elif not user.admin:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")

    session.delete(product)
    session.commit()
    return {"message": "Product removed successfully"}
