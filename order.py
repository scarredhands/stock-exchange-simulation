
from datetime import datetime

class Order:
    def __init__(self, trader, stock, price, quantity, order_type):
        self.trader = trader
        self.stock = stock
        self.price = price
        self.quantity = quantity
        self.order_type = order_type
        self.timestamp = datetime.now()

    def __lt__(self, other):
        if self.order_type == 'buy':
            return (self.price, other.timestamp) > (other.price, self.timestamp)
        return (self.price, self.timestamp) < (other.price, other.timestamp)

    def __repr__(self):
        return f"{self.order_type.upper()} {self.quantity} {self.stock} @ ${self.price:.2f}"
