from fastapi import APIRouter, HTTPException, Depends
from models import User, cart, order, Product
from schemas import cartSchema, productSchema, UserSchema, OrderSchema
from sqlalchemy.orm import Session
from dependecies import verify_token, get_session

order_routes = APIRouter(prefix="/orders", tags=["Orders"])


@order_routes.get("/")
async def order():
    return {"message": "Order route created"}


@order_routes.post("/order/Cart/Add_Item")
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


@order_routes.post("/order/remover_item_cart")
async def remover_item_cart(cart_id: int, session: Session = Depends(get_session),
                            user: User = Depends(verify_token)):
    cart_item = session.query(cart).filter(cart.id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=400, detail="product not found or user whithout permission")
    elif not user.admin or cart_item.user != user:
        raise HTTPException(status_code=400, detail="You do not have permission to make this change")



@order_routes.post("/order/Creat_Order")
async def Creat_Order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = order(user=order_schema.user)
    session.add(new_order)
    session.commit()
    return {"message": "Order created"}


@order_routes.post("/order/cancel/order")
async def cancel_Order(ordr_id: int, session: Session = Depends(get_session),
                       user: User = Depends(verify_token)):
    order_user = session.query(order).filter(order.id == ordr_id).first()
    if not order_user:
        raise HTTPException(status_code=400, detail="Order not found")
    elif not user.admin and order_user.user != user:
        raise HTTPException(status_code=400, detail="You do not have permission to make this change.")

    order_user.status = "CANCELLED"
    session.commit()

    return {
        "message": f"Order ID:{ordr_id} successfully canceled",
        "order": order_user
    }


@order_routes.get("/order/view_my_cart")
async def view_my_cart(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    Cart_item = session.query(cart).filter(cart.user == user.id).all()
    return {
        "user": user.id,
        "name": user.name,
        "cart": Cart_item
    }
