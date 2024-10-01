# # File: predict_stock.py
# import pandas as pd
# import statsmodels.api as sm
# import matplotlib.pyplot as plt

# def predict_stock_price(stock_name):
#     # Load historical data
#     df = pd.read_csv(f'data/{stock_name}.csv', index_col='Date', parse_dates=True)
#     df = df[['Close']]  # We will predict based on 'Close' prices

#     # Fit ARIMA model
#     model = sm.tsa.ARIMA(df['Close'], order=(5, 1, 0))  # (p,d,q) order can be adjusted
#     model_fit = model.fit()

#     # Make prediction
#     forecast = model_fit.forecast(steps=30)  # Predict for the next 30 days
#     forecast_dates = pd.date_range(df.index[-1], periods=30, freq='B')

#     # Plot historical data and forecast
#     plt.figure(figsize=(10, 6))
#     plt.plot(df.index, df['Close'], label="Historical Price")
#     plt.plot(forecast_dates, forecast, label="Predicted Price")
#     plt.title(f"Stock Price Prediction for {stock_name}")
#     plt.xlabel("Date")
#     plt.ylabel("Price")
#     plt.legend()
#     plt.savefig(f'predictions/{stock_name}_prediction.png')
#     plt.show()

# if __name__ == "__main__":
#     stock_name = 'AAPL'  # Test with Apple stock
#     predict_stock_price(stock_name)

import pandas as pd
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt

def predict_stock_price(stock_name):
    # Load historical data
    df = pd.read_csv(f'data/{stock_name}.csv', index_col='Date', parse_dates=True)
    df = df[['Close']]  # We will predict based on 'Close' prices

    # Ensure the date index has a business day frequency
    df = df.asfreq('B')  # 'B' stands for business days

    # Fit ARIMA model
    model = sm.tsa.ARIMA(df['Close'], order=(5, 1, 0))  # (p,d,q) order can be adjusted
    model_fit = model.fit()

    # Make prediction
    forecast = model_fit.forecast(steps=30)  # Predict for the next 30 business days
    forecast_dates = pd.date_range(df.index[-1], periods=30, freq='B')  # Use business day frequency

    # Plot historical data and forecast
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Close'], label="Historical Price")
    plt.plot(forecast_dates, forecast, label="Predicted Price")
    plt.title(f"Stock Price Prediction for {stock_name}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    
    # Create predictions directory if it doesn't exist
    predictions_dir = 'predictions'
    if not os.path.exists(predictions_dir):
        os.makedirs(predictions_dir)
    
    # Save the plot to a file
    plt.savefig(f'{predictions_dir}/{stock_name}_prediction.png')
    plt.show()

if __name__ == "__main__":
    stock_name = 'AAPL'  # Test with Apple stock
    predict_stock_price(stock_name)

