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

    for _ in range(total_seconds):  # Simulating 23,400 trades (1 per second)
        for trader in traders:
            trader.trade()  # Execute trade
        
        current_time += timedelta(seconds=1)  # Move time forward by 1 second
        time.sleep(0.0001)  # Speed up simulation (adjust as needed)

    exchange.cancel_all_orders()
    print("Trading Day Over.")

    for trader in traders:
        initial_value = trader.cash + trader.get_portfolio_value()
        final_value = trader.cash + trader.get_portfolio_value()
        profit_loss = final_value - initial_value
        print(f"Trader {trader.trader_id} Final Portfolio Value: ${final_value:.2f}")
        print(f"Trader {trader.trader_id} Profit/Loss: ${profit_loss:.2f}")

if __name__ == '__main__':
    simulate_trading_day()


# import time
# import random
# from datetime import datetime, timedelta
# from trader import Trader
# from exchange import StockExchange
# from constants import TRADING_START, TRADING_END

# def simulate_trading_day():
#     exchange = StockExchange()
#     traders = [Trader(i + 1, random.randint(5000, 500000), exchange) for i in range(5)]

#     current_time = datetime.combine(datetime.now().date(), TRADING_START)
#     end_time = datetime.combine(datetime.now().date(), TRADING_END)
#     i=0
#     while i<30:
#         for trader in traders:
#             trader.trade()
            
        
#         current_time += timedelta(seconds=1)
#         time.sleep(0.1)  # Simulate time passing, but speed up for testing
#         i+=1
#     exchange.cancel_all_orders()
#     print("Trading Day Over.")
#     for trader in traders:
#         initial_value = trader.cash + trader.get_portfolio_value()
#         final_value = trader.cash + trader.get_portfolio_value()
#         profit_loss = final_value - initial_value
#         print(f"Trader {trader.trader_id} Final Portfolio Value: ${final_value:.2f}")
#         print(f"Trader {trader.trader_id} Profit/Loss: ${profit_loss:.2f}")

# if __name__ == '__main__':
#     simulate_trading_day()


# from flask import Flask, request, jsonify
# from flask_socketio import SocketIO
# from flask_cors import CORS
# import random
# import time
# from datetime import datetime
# from trader import Trader
# from exchange import StockExchange

# app = Flask(__name__)
# CORS(app)  # Enable CORS
# socketio = SocketIO(app, cors_allowed_origins="*")  # Allow WebSocket connections from any origin

# # Initialize Stock Exchange and Traders
# exchange = StockExchange()
# traders = {i: Trader(i, random.randint(5000, 500000), exchange) for i in range(1, 6)}

# def simulate_trading():
#     """ Simulates trading for 6.5 hours (23,400 seconds) """
#     for _ in range(30):  # Simulate for a shorter time for testing
#         for trader in traders.values():
#             stock = random.choice(list(trader.portfolio.keys()))
#             order_type = random.choice(["buy", "sell"])
#             trade_result = trader.trade(stock, order_type)

#             if trade_result:
#                 socketio.emit("trade_update", {"message": trade_result})  # Send updates to frontend

#         time.sleep(1)  # Simulate time delay

# @app.route('/market_summary', methods=['GET'])
# def market_summary():
#     return jsonify(exchange.get_market_summary())

# if __name__ == '__main__':
#     socketio.start_background_task(simulate_trading)  # Run trading simulation
#     socketio.run(app, debug=True, host="0.0.0.0", port=5002)
