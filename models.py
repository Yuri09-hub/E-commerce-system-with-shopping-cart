from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

database = create_engine("sqlite:///database.db")

base = declarative_base()


class Product(base):
    __tablename__ = "products"

    code_product = Column("Product_Code", Integer, primary_key=True)
    name = Column("Product_Name", String, nullable=False)
    description = Column("Description", String)
    stock = Column("Stock", Integer, nullable=False)
    category = Column("Category", String, nullable=False)


#User
class User(base):
    __tablename__ = "users"

    id = Column("ID_User", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String, nullable=False)
    email = Column("Email", String, unique=True, nullable=False)
    password = Column("Password", String, nullable=False)
    street = Column("Street", String, nullable=False)
    city = Column("City", String, nullable=False)
    province = Column("Province", String, nullable=False)
    phone = Column("Phone", String)

    def __init__(self, name, email, password, street, city, province, phone):
        self.name = name
        self.email = email
        self.password = password
        self.street = street
        self.city = city
        self.province = province
        self.phone = phone

class item_cart()
