# # File: fetch_data.py
# import yfinance as yf
# import pandas as pd
# import os

# # Define top 20 US stocks (You can change this list as needed)
# stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'JNJ', 'WMT', 'PG', 'MA', 'DIS', 'NFLX', 'HD', 'PFE', 'KO', 'PEP', 'MRK']

# # Download historical data for each stock
# def fetch_stock_data(stocks):
#     stock_data = {}
#     for stock in stocks:
#         data = yf.download(stock, period='5y')  # Fetch data for the last 5 years
#         stock_data[stock] = data
#     return stock_data

# if __name__ == "__main__":
#     stock_data = fetch_stock_data(stocks)
#     for stock, data in stock_data.items():
#         data.to_csv(f'data/{stock}.csv')  # Save data to a CSV file


import os
import yfinance as yf
import pandas as pd

# Define top 50 US stocks (You can change this list as needed)
stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'JNJ', 'WMT', 
          'PG', 'MA', 'DIS', 'NFLX', 'HD', 'PFE', 'KO', 'PEP', 'MRK', 'XOM', 'BAC', 'CVX', 'NKE', 'CSCO', 'ABT', 'TMO', 'LLY', 'ORCL', 'UNH',
        'BABA', 'CRM', 'COST', 'QCOM', 'INTC', 'MDT', 'MCD', 'TMUS', 'UPS', 'HON',
        'IBM', 'AMD', 'DHR', 'TXN', 'NEE', 'SPGI', 'SBUX', 'BLK', 'GS', 'LOW']

# Create the data directory if it doesn't exist
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Download historical data for each stock
def fetch_stock_data(stocks):
    stock_data = {}
    for stock in stocks:
        print(f"Fetching data for {stock}...")
        data = yf.download(stock, period='5y')  # Fetch data for the last 5 years
        stock_data[stock] = data
    return stock_data

if __name__ == "__main__":
    stock_data = fetch_stock_data(stocks)
    for stock, data in stock_data.items():
        file_path = os.path.join(data_dir, f'{stock}.csv')
        print(f"Saving data to {file_path}")
        data.to_csv(file_path)  # Save data to a CSV file

