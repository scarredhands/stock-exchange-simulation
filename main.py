# import random
# import time
# from datetime import datetime, timedelta
# from trader import Trader
# from exchange import StockExchange
# from constants import TRADING_START, TRADING_END

# def simulate_trading_day():
#     exchange = StockExchange()
#     traders = [Trader(i + 1, random.randint(5000, 500000), exchange) for i in range(5)]

#     current_time = datetime.combine(datetime.now().date(), TRADING_START)
#     end_time = datetime.combine(datetime.now().date(), TRADING_END)
    
#     total_seconds = int((end_time - current_time).total_seconds())  # 6.5 * 60 * 60 = 23400 trades

#     for _ in range(total_seconds):  # Simulating 23,400 trades (1 per second)
#         for trader in traders:
#             trader.trade()  # Execute trade
        
#         current_time += timedelta(seconds=1)  # Move time forward by 1 second
#         time.sleep(0.0001)  # Speed up simulation (adjust as needed)

#     exchange.cancel_all_orders()
#     print("Trading Day Over.")

#     for trader in traders:
#         initial_value = trader.cash + trader.get_portfolio_value()
#         final_value = trader.cash + trader.get_portfolio_value()
#         profit_loss = final_value - initial_value
#         print(f"Trader {trader.trader_id} Final Portfolio Value: ${final_value:.2f}")
#         print(f"Trader {trader.trader_id} Profit/Loss: ${profit_loss:.2f}")
#         log_message = (f"📊 Trader {trader.trader_id} Final Portfolio Value: ${final_value:.2f}\n"
#                        f"💰 Profit/Loss: ${profit_loss:.2f}\n")

#         # print(log_message)
#         exchange.log_trade(log_message) 

# if __name__ == '__main__':
#     simulate_trading_day()


import random
import time
from datetime import datetime, timedelta
from trader import Trader
from exchange import StockExchange
from constants import TRADING_START, TRADING_END

def simulate_trading_day():
    exchange = StockExchange()
    traders = [Trader(i + 1, random.randint(5000, 500000), exchange) for i in range(5)]

    current_time = datetime.combine(datetime.now().date(), TRADING_START)
    end_time = datetime.combine(datetime.now().date(), TRADING_END)

    total_seconds = int((end_time - current_time).total_seconds())  # 6.5 * 60 * 60 = 23400 trades

    # Store initial portfolio values before trading begins
    initial_values = {trader.trader_id: trader.cash + trader.get_portfolio_value() for trader in traders}

    for _ in range(total_seconds):  # Simulating 23,400 trades (1 per second)
        for trader in traders:
            trader.trade()  # Execute trade
        
        current_time += timedelta(seconds=1)  # Move time forward by 1 second
        time.sleep(0.0001)  # Speed up simulation (adjust as needed)

    exchange.cancel_all_orders()
    print("Trading Day Over.")
    exchange.log_trade("📢 Trading Day Over.")

    # Log final portfolio values and profit/loss
    for trader in traders:
        final_value = trader.cash + trader.get_portfolio_value()
        profit_loss = final_value - initial_values[trader.trader_id]  

        log_message = (f"📊 Trader {trader.trader_id} Final Portfolio Value: ${final_value:.2f}\n"
                       f"💰 Profit/Loss: ${profit_loss:.2f}\n")

        print(log_message)
        exchange.log_trade(log_message)  # Log to file

if __name__ == '__main__':
    simulate_trading_day()
