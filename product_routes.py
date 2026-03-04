from fastapi import APIRouter, Depends, HTTPException
from schemas import productSchema
from dependecies import get_session, verify_token
from sqlalchemy.orm import Session
from models import Product, User

product_routes = APIRouter(prefix="/product", tags=["product"])

#rota descenessária
@product_routes.get("/")
async def product():
    return {"message": "Product route created successfully"}

    

#falta rota de atualizar produto,eliminar produtos e buscar produto por id

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
    products = session.query(Product).all() #você usou query all, mas o ideal é usar query limit e offset para paginar os resultados
    #se tiver 1000 produtos , você vai carregar todos os produtos na memória, o que é muito custoso e vai te dar problemas de 
    #performance e escalabilidade
    #o ideal é usar query limit e offset para paginar os resultados
    #ex: products = session.query(Product).limit(10).offset(0)
    #ex: products = session.query(Product).limit(10).offset(10)
   
    return {
        "products": products
    }
