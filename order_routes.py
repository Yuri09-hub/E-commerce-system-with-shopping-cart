from fastapi import FastAPI, APIRouter

order_routes = APIRouter(prefix="/orders", tags=["Orders"])


@order_routes.get("/")
async def order():
    return {"message": "Order route created"}

