from fastapi import APIRouter, Depends, HTTPException
from schemas import cartSchema
from sqlalchemy.orm import Session
from models import User, Product, cart, product_output, product_entry
from dependecies import verify_token, get_session

customer_router = APIRouter(prefix="/customer", tags=["Customer"])


@customer_router.post("/Add_Item")
async def add_item_Cart(cart_schema: cartSchema, session: Session = Depends(get_session),
                        user: User = Depends(verify_token)):
    item = session.query(Product).filter(Product.id == cart_schema.id,
                                         Product.name == cart_schema.product).first()
    if not item:
        raise HTTPException(status_code=400, detail="Product not found")
    entry = 0
    output = 0
    verify_product1 = session.query(product_entry).filter(product_entry.product_id == item.id,
                                                          product_entry.product == item.name).all()
    verify_product2 = session.query(product_output).filter(product_output.product_id == item.id,
                                                          product_output.product == item.name).all()
    if not verify_product1:
        raise HTTPException(status_code=400, detail="Product out of stock")
    if verify_product2:
        for amount1 in verify_product1:
            entry += amount1.amount
        for amount2 in verify_product2:
            output += amount2.amount
        stock = entry - output
        if stock == 0:
            raise HTTPException(status_code=400, detail="Product out of stock")
        elif stock < cart_schema.amount:
            raise HTTPException(status_code=400,
                                detail=f"Insufficient stock. Available: {stock}, requested: {cart_schema.amount}.")

    cart_item = cart(product=item.name, amount=cart_schema.amount, unit_price=item.price, user=user.id,
                     product_id=item.id)
    session.add(cart_item)
    session.commit()

    return {
        "message": "Item added",
        "user": user.id,
        "name": user.name
    }


@customer_router.post("/remover_item_cart")
async def remover_item_cart(cart_id: int, session: Session = Depends(get_session),
                            user: User = Depends(verify_token)):
    cart_item = session.query(cart).filter(cart.id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=400, detail="product not found or user without permission")
    elif not user.admin or cart_item.user != user:
        raise HTTPException(status_code=400, detail="You do not have permission to make this change")


@customer_router.get("/view_my_cart")
async def view_my_cart(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    Cart_item = session.query(cart).filter(cart.user == user.id).all()
    return {
        "user": user.id,
        "name": user.name,
        "cart": Cart_item
    }
