from fastapi import APIRouter

auth_routes = APIRouter(prefix="/auth", tags=["Auth"])


@auth_routes.get("/")
async def auth():
    return {"message": "Auth route created"}
