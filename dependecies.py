from sqlalchemy.orm import sessionmaker, Session
from models import db
from main import oauth2_scheme, SECRET_KEY, ALGORITHM
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from models import User


def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verify_token(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dict_info.get("sub"))
    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401, detail="ERROR")

    user = session.query(User).filter(user_id == User.id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Access Denied")
    else:
        return user


def validate_province(province):
    province_angola = [
        "Bengo",
        "Benguela", "Bié", "Cabinda",
        "Cuando", "Cuanza Norte", "Cuanza Sul",
        "Cubango",  # Nova província (ex-Cuando Cubango)
        "Cunene", "Huambo", "Huíla",
        "Ícolo E Bengo",  # Nova província (ex-Luanda)
        "Luanda", "Lunda Norte", "Lunda Sul",
        "Malanje", "Moxico",
        "Moxico Leste",  # Nova província (ex-Moxico)
        "Namibe", "Uíge",
        "Zaire"]
    if province in province_angola:
        return province
    else:
        return None


def calculate_freight(province):
    fees = {
        "Luanda": 1500, "Icolo e Bengo": 2500, "Bengo": 3000,
        "Benguela": 4000, "Bié": 4500, "Cabinda": 7500,
        "Cuando": 6500, "Cubango": 6500, "Cuanza Norte": 3500,
        "Cuanza Sul": 3500, "Cunene": 6000, "Huambo": 4500,
        "Huíla": 5500, "Lunda Norte": 6500, "Lunda Sul": 6500,
        "Malanje": 4000, "Moxico": 6000, "Moxico Leste": 7000,
        "Namibe": 6000, "Uíge": 4500, "Zaire": 4500
    }

    if province in fees:
        return fees.get(province)
    else:
        return None
