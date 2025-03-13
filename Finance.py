import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st

class FinancialAnalyzer:
    def __init__(self):
        self.portfolio = {}

    def add_asset(self, ticker, weight):
        if not ticker or weight <= 0 or weight > 1:
            return False
        self.portfolio[ticker] = weight
        return True

    def get_portfolio(self):
        return self.portfolio

class BusinessHealthAnalyzer:
    def __init__(self, revenue, expenses, assets, liabilities):
        self.revenue = revenue
        self.expenses = expenses
        self.assets = assets
        self.liabilities = liabilities

    def calculate_profit_margin(self):
        return (self.revenue - self.expenses) / self.revenue if self.revenue > 0 else None

    def calculate_debt_to_equity(self):
        return self.liabilities / (self.assets - self.liabilities) if self.assets > self.liabilities else None

    def calculate_current_ratio(self):
        return self.assets / self.liabilities if self.liabilities > 0 else None

    def assess_health(self):
        profit_margin = self.calculate_profit_margin()
        debt_to_equity = self.calculate_debt_to_equity()
        current_ratio = self.calculate_current_ratio()
        
        if None in [profit_margin, debt_to_equity, current_ratio]:
            return "Invalid Input Values"
        
        health_score = profit_margin * 50 - debt_to_equity * 20 + current_ratio * 30
        
        if health_score > 70:
            return "Healthy Business"
        elif health_score > 40:
            return "Moderate Risk"
        else:
            return "High Risk"

def main():
    st.set_page_config(page_title="Financial Dashboard", layout="wide")
    
    # Initialize session state for portfolio if it doesn't exist
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = FinancialAnalyzer()

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Portfolio Management")
        ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)")
        weight = st.number_input("Enter Portfolio Weight (0-1)", min_value=0.0, max_value=1.0, step=0.01)
        
        if st.button("Add Asset"):
            if st.session_state.portfolio.add_asset(ticker, weight):
                st.success(f"Added {ticker} with weight {weight}")
            else:
                st.error("Invalid Ticker or Weight")
        
        if st.button("View Portfolio"):
            current_portfolio = st.session_state.portfolio.get_portfolio()
            if current_portfolio:
                st.write("Current Portfolio:")
                st.write(current_portfolio)
            else:
                st.write("No assets added yet.")
        
        if st.button("Market Trades"):
            trades = [
                {"Stock": "AAPL", "Action": "Buy", "Price": 150},
                {"Stock": "TSLA", "Action": "Sell", "Price": 800},
                {"Stock": "MSFT", "Action": "Buy", "Price": 280},
                {"Stock": "GOOGL", "Action": "Sell", "Price": 2700},
                {"Stock": "AMZN", "Action": "Buy", "Price": 3300},
                {"Stock": "NFLX", "Action": "Sell", "Price": 500},
                {"Stock": "NVDA", "Action": "Buy", "Price": 220},
                {"Stock": "FB", "Action": "Sell", "Price": 320},
                {"Stock": "BRK.A", "Action": "Buy", "Price": 450000},
                {"Stock": "V", "Action": "Sell", "Price": 220}
            ]
            st.write("Recent Market Trades:")
            st.write(pd.DataFrame(trades))
    
    with col2:
        st.header("Business Health Analysis")
        revenue = st.number_input("Enter Revenue", value=500000)
        expenses = st.number_input("Enter Expenses", value=300000)
        assets = st.number_input("Enter Total Assets", value=700000)
        liabilities = st.number_input("Enter Total Liabilities", value=200000)
        
        if st.button("Assess Business Health"):
            business = BusinessHealthAnalyzer(revenue, expenses, assets, liabilities)
            health_status = business.assess_health()
            if health_status == "Invalid Input Values":
                st.error("Check input values! Revenue, Assets, and Liabilities must be valid.")
            else:
                st.write("Business Health Status:", health_status)

if __name__ == '__main__':
    main()