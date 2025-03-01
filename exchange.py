# import heapq
# from collections import defaultdict
# from datetime import datetime
# from market import MarketData
# from constants import TRADING_START, TRADING_END

# class StockExchange:
#     def __init__(self):
#         self.order_book = {'buy': defaultdict(list), 'sell': defaultdict(list)}
#         self.market_data = MarketData()

#     def is_trading_hours(self):
#         now = datetime.now().time()
#         return TRADING_START <= now<= TRADING_END

#     def accept_order(self, order):
#         if not self.is_trading_hours():
#             print(f"❌ Order rejected (Market Closed) -> {order}")
#             return False

#         heapq.heappush(self.order_book[order.order_type][order.stock], order)
#         self.market_data.update_last_price(order.stock, order.price)
#         self.market_data.update_order_book_summary(order.stock, order.order_type, order.price, order.quantity)
#         print(f"✅ Order accepted -> {order}")
#         self.match_orders(order.stock)
#         return True

#     # def match_orders(self, stock):
#     #     buy_orders = self.order_book['buy'][stock]
#     #     sell_orders = self.order_book['sell'][stock]

#     #     while buy_orders and sell_orders:
#     #         best_buy = heapq.heappop(buy_orders)
#     #         best_sell = heapq.heappop(sell_orders)

#     #         if best_buy.price >= best_sell.price:
#     #             trade_price = (best_buy.price + best_sell.price) / 2
#     #             best_buy.trader.execute_trade(best_buy, trade_price)
#     #             best_sell.trader.execute_trade(best_sell, trade_price)

#     #             self.market_data.update_last_price(stock, trade_price)
#     #             print(f"🔄 Trade Executed: {stock} at ${trade_price:.2f}")
#     #         else:
#     #             heapq.heappush(buy_orders, best_buy)
#     #             heapq.heappush(sell_orders, best_sell)
#     #             break
#     def match_orders(self, stock):
#     buy_orders = self.order_book['buy'][stock]
#     sell_orders = self.order_book['sell'][stock]

#     while buy_orders and sell_orders:
#         best_buy = heapq.heappop(buy_orders)
#         best_sell = heapq.heappop(sell_orders)

#         if best_buy.price >= best_sell.price:
#             trade_price = (best_buy.price + best_sell.price) / 2
#             buyer = best_buy.trader
#             seller = best_sell.trader

#             # Execute trade by passing both buyer and seller
#             buyer.execute_trade(best_buy, trade_price, seller)
#             seller.execute_trade(best_sell, trade_price, buyer)

#             self.market_data.update_last_price(stock, trade_price)
#             print(f"🔄 Trade Executed: {stock} at ${trade_price:.2f}")
#         else:
#             heapq.heappush(buy_orders, best_buy)
#             heapq.heappush(sell_orders, best_sell)
#             break

#     def cancel_all_orders(self):
#         for order_type in self.order_book:
#             for stock in self.order_book[order_type]:
#                 for order in self.order_book[order_type][stock]:
#                     order.trader.notify_order_cancelled(order)
#         self.order_book = {'buy': defaultdict(list), 'sell': defaultdict(list)}
#         print("❌ All pending orders cancelled.")

#     def get_best_bid_offer(self, stock):
#         top_bids_offers = self.market_data.get_top_bids_offers(stock)
#         return {
#             "best_bid": top_bids_offers["top_bids"][0] if top_bids_offers["top_bids"] else None,
#             "best_offer": top_bids_offers["top_offers"][0] if top_bids_offers["top_offers"] else None
#         }
import heapq
from collections import defaultdict
from datetime import datetime
from market import MarketData
from constants import TRADING_START, TRADING_END

class StockExchange:
    def __init__(self):
        self.order_book = {'buy': defaultdict(list), 'sell': defaultdict(list)}
        self.market_data = MarketData()

    def get_market_summary(self):
        """Returns last traded prices and best bids/offers for all stocks"""
        stocks = list(self.market_data.last_traded_price.keys())  # Get list of all stocks

        return {
            "last_prices": self.market_data.last_traded_price,
            "top_bids_offers": {stock: self.market_data.get_top_bids_offers(stock) for stock in stocks}
        }

    def is_trading_hours(self):
        now = datetime.now().time()
        return TRADING_START <= now <= TRADING_END
    
    @staticmethod
    def log_trade(message):
        """Function to store trade logs in a file."""
        with open("trade_logs.txt", "a") as log_file:
            log_file.write(message + "\n")
        print(message, flush=True)  # Also print to terminal (optional)

    def accept_order(self, order):
        if not self.is_trading_hours():
            self.log_trade(f"❌ Order rejected (Market Closed) -> {order}")
            return False

        heapq.heappush(self.order_book[order.order_type][order.stock], order)
        self.market_data.update_last_price(order.stock, order.price)
        self.market_data.update_order_book_summary(order.stock, order.order_type, order.price, order.quantity)

        self.log_trade(f"✅ Order accepted -> {order}")
        self.match_orders(order.stock)
        return True

    def match_orders(self, stock):
        buy_orders = self.order_book['buy'][stock]
        sell_orders = self.order_book['sell'][stock]

        while buy_orders and sell_orders:
            best_buy = heapq.heappop(buy_orders)
            best_sell = heapq.heappop(sell_orders)

            if best_buy.price >= best_sell.price:
                trade_price = (best_buy.price + best_sell.price) / 2
                buyer = best_buy.trader
                seller = best_sell.trader

                # Execute trade by passing both buyer and seller
                buyer.execute_trade(best_buy, trade_price, seller)
                seller.execute_trade(best_sell, trade_price, buyer)

                self.market_data.update_last_price(stock, trade_price)
                self.log_trade(f"🔄 Trade Executed: {stock} at ${trade_price:.2f}")
            else:
                heapq.heappush(buy_orders, best_buy)
                heapq.heappush(sell_orders, best_sell)
                break

    def cancel_all_orders(self):
        for order_type in self.order_book:
            for stock in self.order_book[order_type]:
                for order in self.order_book[order_type][stock]:
                    order.trader.notify_order_cancelled(order)
        self.order_book = {'buy': defaultdict(list), 'sell': defaultdict(list)}
        self.log_trade("❌ All pending orders cancelled.")

    def get_best_bid_offer(self, stock):
        top_bids_offers = self.market_data.get_top_bids_offers(stock)
        return {
            "best_bid": top_bids_offers["best_bid"][0] if top_bids_offers["best_bid"] else None,
            "best_offer": top_bids_offers["best_offer"][0] if top_bids_offers["best_offer"] else None
        }
