from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
import secrets

db = create_engine("sqlite:///database.db")

base = declarative_base()


class Product(base):
    __tablename__ = "products"

    code_product = Column("Product_Code", Integer, primary_key=True)
    price = Column("price", Float, nullable=False)
    name = Column("product_name", String, nullable=False)
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

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String, nullable=False)
    email = Column("Email", String, unique=True, nullable=False)
    password = Column("Password", String, nullable=False)
    street = Column("Street", String)
    city = Column("City", String)
    province = Column("Province", String, nullable=False)
    phone = Column("Phone", String)
    admin = Column("admin", Boolean, default=False)
    active = Column("active", Boolean)

    def __init__(self, name, email, password, street, city, province, phone, admin=False, active=True):
        self.name = name
        self.email = email
        self.password = password
        self.street = street
        self.city = city
        self.province = province
        self.phone = phone
        self.active = active
        self.admin = admin


class order(base):
    __tablename__ = "orders"

    id = Column("id_order", Integer, primary_key=True, autoincrement=True)
    user = Column("user_id", ForeignKey("users.id"))
    price = Column("total_price", Float)
    status = Column("Status", String, nullable=False)
    payment = Column("payment", String, nullable=False)
    items = Relationship("cart", cascade="all, delete")

    # item_cart

    def __init__(self, user, payment, status="PENDING", price=0):
        self.user = user
        self.status = status
        self.price = price
        self.payment = payment

    def calculate_total_price(self):
        return sum(item.unit_price * item.amount for item in self.items)


class cart(base):
    __tablename__ = "cart"

    id = Column("id_cart", Integer, primary_key=True, autoincrement=True)
    user = Column("user", ForeignKey("users.id"))
    product = Column("Product", String)
    amount = Column("amount", Integer)
    unit_price = Column("unit_price", Float)

    def __int__(self, product, amount, unit_price):
        self.product = product
        self.amount = amount
        self.unit_price = unit_price


class cupom:
    @staticmethod
    def generate_cupom():
        return secrets.token_urlsafe(8)
