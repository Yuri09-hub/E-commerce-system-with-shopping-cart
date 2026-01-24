from models import User, cupom, order, cart
from sqlalchemy.orm import session


class store:
    @staticmethod
    def pay_single_oder(orde_id,session):
        try:
            Session = session.query(order).filter(order.id == orde_id).filter(order.status == 'PENDING').all()

        finally: