from fastapi import APIRouter, HTTPException, Depends
from models import User, cart, order, Product, product_entry, product_output, cupom
from schemas import cartSchema, productSchema, UserSchema, OrderSchema
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from dependecies import verify_token, get_session
from datetime import timezone, datetime, timedelta

order_routes = APIRouter(prefix="/orders", tags=["Orders"])


@order_routes.post("/order/Creat_Order")
async def Creat_Order(session: Session = Depends(get_session),
                      user: User = Depends(verify_token)):
    price = 0
    item_order = session.query(cart).filter(cart.user == user.id).all()
    if not item_order:
        raise HTTPException(status_code=400, detail="item(s) not found")
    if user.admin:
        raise HTTPException(status_code=400, detail="You do not have permission to make this change")

    for item in item_order:
        new_order = order(user=item.user, price=(item.unit_price * item.amount))

        price += new_order.price
        session.add(new_order)

    session.query(cart).filter(cart.user == user.id).delete()
    session.commit()
    orders = session.query(order).all()
    return {"message": "Order created",
            "user": user.id,
            "name": user.name,
            "order": orders,
            "total": price
            }


@order_routes.get("/order/view_my_order")
async def view_my_order(user_id: int, session: Session = Depends(get_session),
                        user: User = Depends(verify_token)):
    order_user = session.query(order).filter(order.user == user_id).all()
    if not order_user:
        raise HTTPException(status_code=400, detail="Order not found")
    elif not user.admin or not user.id != user:
        raise HTTPException(status_code=400, detail="You do not have permission to make this change")

    return order_user


@order_routes.post("/order/finalize")
async def finalize(ordr_id: int, session: Session = Depends(get_session)):
    order_user = session.query(order).filter(order.id == ordr_id).first()
    if not order_user:
        raise HTTPException(status_code=400, detail="Order not found")
    order_user.status = "FINALIZED"
    cart_item = session.query(cart).filter(cart.user == order_user.user).all()
    if cart_item:
        for item in cart_item:
            out = product_output(product=item.product_id, amount=item.amount, date=datetime.now(timezone.utc))
            session.add(out)
            session.delete(item)
    session.commit()
    user = session.query(order).filter(order.user == order_user.user, order.status == "FINALIZED").count()
    if user and user % 5 == 0:
        deadline = (datetime.now(timezone.utc) + timedelta(days=4))
        code = cupom.generate_cupom()
        new_cupom = cupom(code=code, discount=0.02, valid_until=deadline, user=order_user.user)
        session.add(new_cupom)
        return {"message": f"Order successfully finalized,Congratulations! "
                           f"You've won a 2% discount coupon valid until {deadline}."}

    return {"message": f"Order successfully finalized"}


@order_routes.post("/order/cancel/order")
async def cancel_Order(ordr_id: int, session: Session = Depends(get_session),
                       user: User = Depends(verify_token)):
    order_user = session.query(order).filter(order.id == ordr_id).first()
    if not order_user:
        raise HTTPException(status_code=400, detail="Order not found")
    elif not user.admin and order_user.user != user:
        raise HTTPException(status_code=400, detail="You do not have permission to make this change.")
    elif order_user.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Order already canceled")
    order_user.status = "CANCELLED"
    cart_item = session.query(cart).filter(cart.user == order_user.user).all()
    if cart_item:
        for item in cart_item:
            session.delete(item)
    session.commit()
    return {
        "message": f"Order ID:{ordr_id} successfully canceled",
    }