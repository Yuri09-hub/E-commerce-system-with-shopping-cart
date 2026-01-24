from models import User, cupom, order, cart


class store:
    def __init__(self, cupom, User, Order, cart):
        self.User = User
        self.Order = Order
        self.cart = cart
        self.cupom = cupom

    def register(self, name, email, password, street, city, province, phone):
        self.User.name = name
        self.User.email = email
        self.User.password = password
        self.User.street = street
        self.User.city = city
        self.User.province = province
        self.User.phone = phone

    def login(self, email, password):
        self.User.email = email
        self.User.password = password
