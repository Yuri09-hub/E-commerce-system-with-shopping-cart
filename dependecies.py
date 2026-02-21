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
        raise HTTPException(status_code=401, detail="Access Denied")

    user = session.query(User).filter(user_id == User.id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Access Denied")
    else:
        return user
