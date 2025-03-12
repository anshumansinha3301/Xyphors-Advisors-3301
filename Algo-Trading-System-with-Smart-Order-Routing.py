import heapq
import numpy as np
import pandas as pd
import random
import threading
from collections import defaultdict
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class OrderBook:
    """ Implements a matching engine using MinHeap & MaxHeap for bid-ask matching. """
    def __init__(self):
        self.buy_orders = []  # MaxHeap for buyers
        self.sell_orders = []  # MinHeap for sellers
        self.trade_history = []

    def place_order(self, trader, order_type, stock, quantity, price):
        order = (-price, trader, stock, quantity) if order_type == "buy" else (price, trader, stock, quantity)
        if order_type == "buy":
            heapq.heappush(self.buy_orders, order)
        else:
            heapq.heappush(self.sell_orders, order)
        self.match_orders()

    def match_orders(self):
        """ Matches buy and sell orders if the prices are compatible. """
        while self.buy_orders and self.sell_orders and -self.buy_orders[0][0] >= self.sell_orders[0][0]:
            buy_price, buyer, stock, buy_qty = heapq.heappop(self.buy_orders)
            sell_price, seller, stock, sell_qty = heapq.heappop(self.sell_orders)
            trade_qty = min(buy_qty, sell_qty)

            self.trade_history.append(f"{buyer} bought {trade_qty} of {stock} from {seller} at {sell_price}")

            if buy_qty > trade_qty:
                heapq.heappush(self.buy_orders, (buy_price, buyer, stock, buy_qty - trade_qty))
            if sell_qty > trade_qty:
                heapq.heappush(self.sell_orders, (sell_price, seller, stock, sell_qty - trade_qty))

class AITradeSignal:
    """ Uses LSTM to predict stock prices and generate trade signals. """
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(10, 1)),
            LSTM(50),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def train_model(self, historical_data):
        X_train = np.array([historical_data[i:i+10] for i in range(len(historical_data)-10)])
        y_train = np.array(historical_data[10:])
        self.model.fit(X_train, y_train, epochs=5, batch_size=1, verbose=0)

    def predict_next_price(self, last_10_prices):
        return self.model.predict(np.array([last_10_prices]).reshape(1, 10, 1))[0][0]

class TradingSystem:
    """ Combines Order Book Matching, AI Trade Signals, and Smart Order Routing """
    def __init__(self):
        self.order_book = OrderBook()
        self.ai_trader = AITradeSignal()
        self.traders = ["Anshu", "Ayush", "Harshit", "Dipanshu"]

    def simulate_market(self):
        """ Simulates stock price movement and AI-based trading decisions. """
        stock_prices = {"AAPL": [random.randint(100, 150) for _ in range(20)]}
        for _ in range(10):
            stock = "AAPL"
            last_prices = stock_prices[stock][-10:]
            predicted_price = self.ai_trader.predict_next_price(last_prices)
            stock_prices[stock].append(predicted_price)

            trader = random.choice(self.traders)
            order_type = "buy" if random.random() > 0.5 else "sell"
            quantity = random.randint(1, 5)
            self.order_book.place_order(trader, order_type, stock, quantity, round(predicted_price, 2))

    def start_trading(self):
        threading.Thread(target=self.simulate_market).start()

# Running the trading system
system = TradingSystem()
system.start_trading()

# Print matched trades after simulation
import time
time.sleep(2)  # Simulate trading time

print("\nTrade History:")
for trade in system.order_book.trade_history:
    print(trade)
