from fastapi import FastAPI, APIRouter, HTTPException, Depends
from models import User, cart, order
from schemas import cartSchema, productSchema, UserSchema
from sqlalchemy.orm import Session
from dependecies import verify_token, get_session

order_routes = APIRouter(prefix="/orders", tags=["Orders"])


@order_routes.get("/")
async def order():
    return {"message": "Order route created"}


@order_routes.post("/order/Add_Item")
async def add_item(id_order: int, Cart: cartSchema, session: Session = Depends(get_session),
                   user: User = Depends(verify_token)):
    Order = session.query()
