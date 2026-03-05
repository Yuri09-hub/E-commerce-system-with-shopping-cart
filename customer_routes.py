from fastapi import APIRouter, Depends, HTTPException
from schemas import cartSchema
from sqlalchemy.orm import Session
from models import User, Product, cart, cupom
from dependecies import verify_token, get_session

customer_router = APIRouter(prefix="/customer", tags=["customer"])


@customer_router.post("/Add_Item")
async def add_item_Cart(product_id: int, cart_schema: cartSchema, session: Session = Depends(get_session),
                        user: User = Depends(verify_token)):
    item = session.query(Product).filter(product_id == Product.code_product).first()
    if not item:
        raise HTTPException(status_code=400, detail="Product not found")
    elif item.stock < cart_schema.amount:
        raise HTTPException(status_code=400, detail="Not enough stock")
    elif item.stock <= 0:
        raise HTTPException(status_code=400, detail="Out of stock")

    cart_item = cart(product=item.name, amount=cart_schema.amount, unit_price=item.price, user=user.id)
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
        raise HTTPException(status_code=400, detail="product not found or user whithout permission")
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
