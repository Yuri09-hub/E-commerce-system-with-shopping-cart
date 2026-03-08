from fastapi import APIRouter, HTTPException, Depends

from models import User, cart, order, product_output, cupom
from sqlalchemy.orm import Session
from dependecies import verify_token, get_session, calculate_freight
from datetime import timezone, datetime, timedelta

order_routes = APIRouter(prefix="/orders", tags=["Orders"])


@order_routes.post("/order/Create_Order")
async def Create_Order(id_user, session: Session = Depends(get_session),
                       user: User = Depends(verify_token)):
    price = 0
    item_order = session.query(cart).filter(cart.user == id_user).all()
    if not item_order:
        raise HTTPException(status_code=400, detail="item(s) not found")

    for item in item_order:
        price += (item.unit_price * item.amount)
    price += calculate_freight(user.province)

    new_order = order(user=item_order[0].user, price=price,
                      freight=calculate_freight(user.province))
    session.add(new_order)

    session.commit()
    orders = session.query(order).filter(order.status == "PENDING").all()
    return {"message": "Order created",
            "user": user.id,
            "name": user.name,
            "order": orders,
            "total": price
            }


@order_routes.post("order/use_coupon")
async def use_coupon(cupom_id: int, code: str, order_id, session: Session = Depends(get_session),
                     user: User = Depends(verify_token)):
    find_coupon = session.query(cupom).filter(cupom.code == code, cupom.id == cupom_id, cupom.user == user.id).first()
    find_order = session.query(order).filter(order.id == order_id).first()
    if not find_coupon:
        raise HTTPException(status_code=400, detail="Coupon not found")
    elif not find_order:
        raise HTTPException(status_code=400, detail="Order not found")
    elif find_coupon.status == "USED":
        raise HTTPException(status_code=400, detail="Coupon used")
    elif not cupom.is_valid(find_coupon.valid_until):
        find_coupon.status = "EXPIRED"
        session.commit()
        raise HTTPException(status_code=400, detail="Expired coupon")

    find_order.price = find_order.price + (find_coupon.discount * find_order.price)
    find_coupon.status = "USED"
    session.commit()
    return {"message": "Coupon used successfully."}


@order_routes.get("order/view_my_order")
async def view_my_order(user_id: int, session: Session = Depends(get_session),
                        user: User = Depends(verify_token)):
    order_user = session.query(order).filter(order.user == user_id).limit(10).offset(0).all()
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

    cart_item = session.query(cart).filter(cart.user == order_user.user).all()
    if not cart_item:
        raise HTTPException(status_code=400, detail=" item(s) not found")

    for item in cart_item:
        today = datetime.now(timezone.utc)
        out = product_output(product_id=item.product_id,
                             amount=item.amount,
                             date=today)
        session.add(out)
        session.delete(item)

    order_user.status = "FINALIZED"
    msg = f"Order successfully finalized"
    session.flush()

    user = session.query(order).filter(order.user == order_user.user,
                                       order.status == "FINALIZED").count()
    if user and user % 5 == 0:
        deadline = (datetime.now(timezone.utc) + timedelta(days=4))
        code = cupom.generate_cupom()
        new_cupom = cupom(code=code, discount=0.02, valid_until=deadline, user=order_user.user)
        session.add(new_cupom)
        msg = f"Order successfully finalized,Congratulations! " \
              f"You've won a 2% discount coupon valid until {deadline}."

    session.commit()
    return {"message": msg}


@order_routes.post("/order/cancel/order")
async def cancel_Order(ordr_id: int, session: Session = Depends(get_session),
                       user: User = Depends(verify_token)):
    order_user = session.query(order).filter(order.id == ordr_id).first()
    if not order_user:
        raise HTTPException(status_code=404, detail="Order not found")
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
