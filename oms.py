from order import Order
import random

class OrderManagementSystem:
    def __init__(self, exchange):
        self.exchange = exchange

    def place_order(self, trader, stock, order_type):
        best_bid_offer = self.exchange.get_best_bid_offer(stock)
        best_bid = best_bid_offer["best_bid"][0] if best_bid_offer["best_bid"] else None
        best_ask = best_bid_offer["best_offer"][0] if best_bid_offer["best_offer"] else None

        if best_bid and best_ask:
            price_options = [best_bid, best_ask, (best_bid + best_ask) / 2]
            price = random.choice(price_options)
        else:
            last_price = self.exchange.market_data.get_last_price(stock)
            price = last_price * (1 + random.choice([-0.05, 0.05]))

        order = Order(trader, stock, price, 1000, order_type)
        return self.exchange.accept_order(order)
