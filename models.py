from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

database = create_engine("sqlite:///database.db")

base = declarative_base()


class Product(base):
    __tablename__ = "products"

    code_product = Column("Product_Code", Integer, primary_key=True)
    price = Column("Price", Float, nullable=False)
    name = Column("Product", String, nullable=False)
    description = Column("Description", String)
    stock = Column("Stock", Integer, nullable=False)
    category = Column("Category", String, nullable=False)

    def __init__(self, price, name, stock, category, description=""):
        self.price = price
        self.name = name
        self.description = description
        self.stock = stock
        self.category = category


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


class item_cart(base):

    def __int__(self, product, amount):
        self.product = product
        self.amount = amount


class cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, amount):
        self.items.append(item_cart(product, amount))

    def total(self):
        return sum(item.subtotal() for item in self.items)


class order(base):
    __tablename__ = "orders"
    id = Column("ID_Order", Integer, primary_key=True, autoincrement=True)
    user = Column("User_Id", ForeignKey("users.id"))
    name = Column("Name_user", ForeignKey("users.name"))
    price = Column("total_price", Float)
