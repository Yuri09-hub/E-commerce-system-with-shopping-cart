from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

database = create_engine("sqlite:///database.db")

base = declarative_base()


#User
class User(base):
    __tablename__ = "users"

    id = Column("ID User", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String)
    email = Column("Email", String, unique=True, nullable=False)
