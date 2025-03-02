
import random
from oms import OrderManagementSystem
from constants import STOCK_SYMBOLS
from exchange import StockExchange

class Trader:
    def __init__(self, trader_id, cash, exchange):
        self.trader_id = trader_id
        self.cash = cash
        self.portfolio = {stock: random.randint(1000, 5000) for stock in STOCK_SYMBOLS}
        self.oms = OrderManagementSystem(exchange)

    def execute_trade(self, order, price, counterparty):
        total_value = price * order.quantity
        exchange = StockExchange()

        if order.order_type == 'buy':
            if self.cash >= total_value:  # Ensure buyer has enough money
                self.cash -= total_value  # Deduct buyer's cash
                counterparty.cash += total_value  # Add money to seller's account
                self.portfolio[order.stock] = self.portfolio.get(order.stock, 0) + order.quantity  # Add shares to buyer
                counterparty.portfolio[order.stock] -= order.quantity  # Deduct shares from seller
                print(f"💰 Trade Complete: {self.trader_id} bought {order.quantity} shares from {counterparty.trader_id} at ${price:.2f}")
                exchange.log_trade(f"💰 Trade Complete: {self.trader_id} bought {order.quantity} shares from {counterparty.trader_id} at ${price:.2f}")
            else:
                print(f"❌ Trader {self.trader_id} has insufficient funds!")
                exchange.log_trade(f"❌ Trader {self.trader_id} has insufficient funds!")

        else:  # Sell order
            if self.portfolio.get(order.stock, 0) >= order.quantity:  # Ensure seller has stocks
                self.cash += total_value  # Seller gets paid
                counterparty.cash -= total_value  # Buyer pays money
                self.portfolio[order.stock] -= order.quantity  # Remove shares from seller
                counterparty.portfolio[order.stock] = counterparty.portfolio.get(order.stock, 0) + order.quantity  # Buyer receives shares
                print(f"💰 Trade Complete: {self.trader_id} sold {order.quantity} shares to {counterparty.trader_id} at ${price:.2f}")
                exchange.log_trade(f"💰 Trade Complete: {self.trader_id} sold {order.quantity} shares to {counterparty.trader_id} at ${price:.2f}")
            else:
                print(f"❌ Trader {self.trader_id} does not have enough stocks to sell!")
                exchange.log_trade(f"❌ Trader {self.trader_id} does not have enough stocks to sell!")

    def trade(self):
        stock = random.choice(STOCK_SYMBOLS)
        exchange = StockExchange()
        order_type = random.choice(['buy', 'sell'])
        last_price = self.oms.exchange.market_data.get_last_price(stock)
        required_cash = last_price * 1000  # Cash needed to buy 1000 stocks

        if order_type == 'buy':
            if self.cash < required_cash:
                if random.choice([True, False]):  # Randomly decide whether to deposit money
                    deposit_amount = required_cash - self.cash
                    print(f"Trader {self.trader_id} needs more cash. Depositing ${deposit_amount:.2f}.")
                    exchange.log_trade(f"Trader {self.trader_id} needs more cash. Depositing ${deposit_amount:.2f}.")
                    self.deposit_cash(deposit_amount)
                else:
                    print(f"Trader {self.trader_id} decided not to deposit money. Skipping trade.")
                    exchange.log_trade(f"Trader {self.trader_id} decided not to deposit money. Skipping trade.")
                    return
            self.oms.place_order(self, stock, order_type)

        elif order_type == 'sell':
            if self.portfolio.get(stock, 0) < 1000:
                print(f"Trader {self.trader_id} does not have enough stocks to sell. Skipping trade.")
                exchange.log_trade(f"Trader {self.trader_id} does not have enough stocks to sell. Skipping trade.")
                return
            self.oms.place_order(self, stock, order_type)

    def notify_order_cancelled(self, order):
        exchange = StockExchange()
        print(f"Trader {self.trader_id} notified: Order cancelled -> {order}")
        exchange.log_trade(f"Trader {self.trader_id} notified: Order cancelled -> {order}")

    def get_portfolio_value(self):
        return sum(self.portfolio.get(stock, 0) * self.oms.exchange.market_data.get_last_price(stock) 
                   for stock in STOCK_SYMBOLS)

    def deposit_cash(self, amount):
        self.cash += amount
        print(f"Trader {self.trader_id} deposited ${amount:.2f}")

    def withdraw_cash(self, amount):
        if amount <= self.cash:
            self.cash -= amount
            print(f"Trader {self.trader_id} withdrew ${amount:.2f}")
        else:
            print(f"Trader {self.trader_id} insufficient funds for withdrawal")
