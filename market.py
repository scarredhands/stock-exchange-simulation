from collections import defaultdict
import random
from constants import STOCK_SYMBOLS

class MarketData:
    def __init__(self):
        self.last_traded_price = {stock: random.randint(100, 150) for stock in STOCK_SYMBOLS}
        self.order_book_summary = {'buy': defaultdict(list), 'sell': defaultdict(list)}

    def update_last_price(self, stock, price):
        self.last_traded_price[stock] = price

    def get_last_price(self, stock):
        return self.last_traded_price[stock]

    def get_top_bids_offers(self, stock):
        """Returns the best bid and offer for a given stock"""
        stock_data = self.order_book_summary.get(stock, {"top_bids": [], "top_offers": []})
        return {
            "best_bid": stock_data["top_bids"][0] if stock_data["top_bids"] else None,
            "best_offer": stock_data["top_offers"][0] if stock_data["top_offers"] else None
        }

    def update_order_book_summary(self, stock, order_type, price, quantity):
        self.order_book_summary[order_type][stock].append((price, quantity))
        self.order_book_summary[order_type][stock].sort(reverse=(order_type == 'buy'))
        self.order_book_summary[order_type][stock] = self.order_book_summary[order_type][stock][:5]
