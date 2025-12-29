from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


database = create_engine("sqlite:///database.db")

base = declarative_base()


