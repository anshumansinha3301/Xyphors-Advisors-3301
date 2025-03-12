import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
from sklearn.ensemble import RandomForestRegressor

class PortfolioOptimizer:
    """ Portfolio optimization using Modern Portfolio Theory & Monte Carlo Simulations """
    def __init__(self, stock_data):
        self.stock_data = stock_data
        self.returns = stock_data.pct_change().dropna()

    def calculate_metrics(self, weights):
        portfolio_return = np.sum(self.returns.mean() * weights) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(self.returns.cov() * 252, weights)))
        sharpe_ratio = portfolio_return / portfolio_volatility
        return portfolio_return, portfolio_volatility, sharpe_ratio

    def optimize_portfolio(self):
        num_assets = len(self.returns.columns)
        initial_weights = np.ones(num_assets) / num_assets
        bounds = tuple((0, 1) for _ in range(num_assets))
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

        def negative_sharpe(weights):
            return -self.calculate_metrics(weights)[2]

        result = minimize(negative_sharpe, initial_weights, bounds=bounds, constraints=constraints)
        return result.x

class MonteCarloSimulation:
    """ Runs Monte Carlo Simulations for risk assessment """
    def __init__(self, stock_data, simulations=10000):
        self.stock_data = stock_data
        self.simulations = simulations
        self.returns = stock_data.pct_change().dropna()

    def run_simulation(self):
        num_assets = len(self.returns.columns)
        results = np.zeros((3, self.simulations))
        for i in range(self.simulations):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            ret, vol, sharpe = PortfolioOptimizer(self.stock_data).calculate_metrics(weights)
            results[0, i], results[1, i], results[2, i] = ret, vol, sharpe
        return results

class AIStockPredictor:
    """ Uses Machine Learning (Random Forest) to predict stock returns """
    def __init__(self, stock_data):
        self.stock_data = stock_data
        self.model = RandomForestRegressor(n_estimators=100)

    def train_model(self):
        X = self.stock_data.shift(1).dropna()
        y = self.stock_data.pct_change().shift(-1).dropna()
        self.model.fit(X, y)

    def predict_next_day(self, latest_data):
        return self.model.predict(np.array([latest_data]))[0]

stocks = pd.DataFrame({
    'AAPL': np.random.uniform(120, 150, 100),
    'GOOGL': np.random.uniform(2200, 2500, 100),
    'TSLA': np.random.uniform(600, 700, 100),
    'MSFT': np.random.uniform(280, 320, 100),
})

# Running Portfolio Optimization
optimizer = PortfolioOptimizer(stocks)
optimal_weights = optimizer.optimize_portfolio()
print("\nOptimal Portfolio Allocation:")
for stock, weight in zip(stocks.columns, optimal_weights):
    print(f"{stock}: {weight:.2%}")

# Running Monte Carlo Simulations
simulator = MonteCarloSimulation(stocks)
results = simulator.run_simulation()
plt.figure(figsize=(10, 6))
plt.scatter(results[1], results[0], c=results[2], cmap='viridis', marker='o', edgecolors='black')
plt.colorbar(label="Sharpe Ratio")
plt.xlabel("Volatility")
plt.ylabel("Return")
plt.title("Monte Carlo Simulation: Risk vs. Return")
plt.show()

ai_predictor = AIStockPredictor(stocks)
ai_predictor.train_model()
predicted_returns = ai_predictor.predict_next_day(stocks.iloc[-1])
print("\nPredicted Next Day Returns:")
for stock, pred in zip(stocks.columns, predicted_returns):
    print(f"{stock}: {pred:.4f}")
