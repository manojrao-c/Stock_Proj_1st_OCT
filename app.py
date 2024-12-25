# # File: app.py
# from flask import Flask, render_template
# import os

# app = Flask(__name__)

# # Home route
# @app.route('/')
# def index():
#     # Get list of prediction images for display
#     predictions = os.listdir('static/predictions')
#     return render_template('index.html', predictions=predictions)

# if __name__ == "__main__":
#     app.run(debug=True)

# import os
# import yfinance as yf
# from flask import Flask, render_template

# app = Flask(__name__)

# def get_top_20_stocks():
#     # Define a list of the top 20 stocks (symbol list)
#     top_20_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC',
#                      'V', 'JPM', 'DIS', 'PYPL', 'BA', 'BABA', 'CSCO', 'PEP', 'KO', 'XOM']

#     stock_data = []

#     for symbol in top_20_stocks:
#         stock = yf.Ticker(symbol)
#         info = stock.info
#         hist = stock.history(period="1d")
#         current_price = hist['Close'][0] if not hist.empty else None
#         stock_data.append({
#             'symbol': symbol,
#             'name': info.get('shortName'),
#             'price': current_price,
#             'market_cap': info.get('marketCap'),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield')
#         })

#     return stock_data

# @app.route('/')
# def index():
#     stocks = get_top_20_stocks()  # Get top 20 stock stats
#     return render_template('index.html', stocks=stocks)

# if __name__ == '__main__':
#     app.run(debug=True)




# import os
# import yfinance as yf
# from flask import Flask, render_template

# app = Flask(__name__)

# def get_top_50_stocks():
#     # List of the top 50 stock symbols
#     top_50_stocks = [
#         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC',
#         'V', 'JPM', 'DIS', 'PYPL', 'BA', 'BABA', 'CSCO', 'PEP', 'KO', 'XOM',
#         'ADBE', 'ORCL', 'PFE', 'ABT', 'MRNA', 'T', 'VZ', 'IBM', 'CRM', 'NKE',
#         'COST', 'WMT', 'HD', 'MCD', 'SBUX', 'CVX', 'HON', 'QCOM', 'TXN', 'AVGO',
#         'SPGI', 'MS', 'GS', 'C', 'BKNG', 'BLK', 'AXP', 'LMT', 'UNH', 'JNJ'
#     ]

#     stock_data = []

#     for symbol in top_50_stocks:
#         stock = yf.Ticker(symbol)
#         info = stock.info
#         # Use the history() method to get the most recent stock price
#         hist = stock.history(period="1d")
#         current_price = hist['Close'][0] if not hist.empty else None
        
#         stock_data.append({
#             'symbol': symbol,
#             'name': info.get('shortName'),
#             'price': current_price,
#             'market_cap': info.get('marketCap'),
#             'pe_ratio': info.get('trailingPE'),
#             'dividend_yield': info.get('dividendYield')
#         })

#     return stock_data


# @app.route('/')
# def index():
#     stocks = get_top_50_stocks()  # Get top 50 stock stats
#     return render_template('index.html', stocks=stocks)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')


from ast import YieldFrom
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import yfinance
import yfinance as yf
import pandas as pd
import os
import time
import threading
import logging
import re

app = Flask(__name__)
app.secret_key = "34uyfhuyjrur43fjbh"
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Initialize the database (run this once)
# @app.before_first_request
# def create_tables():
#     db.create_all()

first_request = True

@app.before_request
def create_tables():
    global first_request
    if first_request:
        db.create_all()
        first_request = False


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # Replace query.get with session.get

# Routes for user authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            login_user(user)
            return redirect(url_for('index'))
        flash('Login failed, check your credentials')
    return render_template('login.html')

def is_password_strong(password):
    """Check if the password meets the strength criteria."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, "Password is strong."

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please log in instead.')
            return redirect(url_for('login'))
        
        # Check password strength
        is_strong, message = is_password_strong(password)
        if not is_strong:
            flash(message)  # Flash the error message
            return render_template('signup.html', username=username)  # Re-render the signup page
        
        # Create new user if username is unique
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username')
    flash('You have been logged out successfully.')
    return redirect(url_for('login'))

fetched_stocks = None
data_loading = True

@app.before_first_request
def initilize():
    global fetched_stocks
    if fetched_stocks is None:
        threading.Thread(target=get_top_stocks).start()

# Home route
@app.route('/')
@login_required
def index():
    # global fetched_stocks
    # if fetched_stocks is None:
    #     fetched_stocks = get_top_stocks(100)  # Fetch top 100 stocks only once
    # return render_template('index.html', stocks=fetched_stocks)
    return render_template('index.html', username=session.get('username'))

# @app.route('/load_stocks')
# @login_required
# def load_stocks():
#     # Get the number of stocks to load from the query parameter
#     num_stocks = int(request.args.get('num', 10))  # Default to 10 stocks
#     stocks = get_top_stocks(num_stocks)  # Get the specified number of stock stats
#     return render_template('stocks_partial.html', stocks=stocks)

@app.route('/load_stocks')
@login_required
def load_stocks():
    try:
        global fetched_stocks
        # num_stocks = int(request.args.get('num', 9))  # Default to 9 stocks
        # total_stocks = 100  # Set the total number of stocks you want to load
        # offset = int(request.args.get('offset', 0))   # Default to offset 0

        # if fetched_stocks is None or offset >= total_stocks:
        #     return ""  # Return an empty response if the offset exceeds total stocks

        # Adjust the stock data based on the offset
        # stocks = fetched_stocks  # Get the next batch of stocks

        # if not stocks:  # If no stocks are returned, return an empty response
        #     return ""  # Return an empty string to indicate no more data

        # Render the partial HTML template
        if fetched_stocks is not None:
            # return fetched_stocks
            return render_template('stocks_partial.html', stocks=fetched_stocks)
        return []
    except Exception as e:
        print(f"Error in /load_stocks: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/data-loading-status', methods=['GET'])
def data_loading_status():
    """Endpoint to check if data is still loading."""
    return jsonify({"loading": data_loading})

# Route for stock details (graphs and information)
@app.route('/stock/<symbol>')
@login_required
def stock_details(symbol):
    stock = yfinance.Ticker(symbol)
    hist = stock.history(period="5y")
    return render_template('stock_details.html', stock=stock, hist=hist)

# Helper function (unchanged)
# def get_top_50_stocks():
#     top_50_stocks = [
#         'AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'JNJ',
#         'WMT', 'PG', 'MA', 'DIS', 'NFLX', 'HD', 'PFE', 'KO', 'PEP', 'MRK', 'XOM',
#         'BAC', 'CVX', 'NKE', 'CSCO', 'ABT', 'TMO', 'LLY', 'ORCL', 'UNH', 'BABA',
#         'CRM', 'COST', 'QCOM', 'INTC', 'MDT', 'MCD', 'TMUS', 'UPS', 'HON',
#         'IBM', 'AMD', 'DHR', 'TXN', 'NEE', 'SPGI', 'SBUX', 'BLK', 'GS', 'LOW'
#     ]
#     stock_data = []

#     for symbol in top_50_stocks:
#         try:
#             stock = yf.Ticker(symbol)
#             info = stock.info
            
#             # Log the symbol and info for debugging
#             if info is None:
#                 print(f"Warning: No info found for {symbol}. Skipping.")
#                 continue

#             hist = stock.history(period="1d")
#             current_price = hist['Close'].iloc[0] if not hist.empty else None

#             stock_data.append({
#                 'symbol': symbol,
#                 'name': info.get('shortName', 'N/A'),
#                 'price': current_price,
#                 'market_cap': info.get('marketCap', 'N/A'),
#                 'pe_ratio': info.get('trailingPE', 'N/A'),
#                 'dividend_yield': info.get('dividendYield', 'N/A')
#             })
#         except Exception as e:
#             print(f"Error retrieving data for {symbol}: {e}")
#             print(f"Response: {info}")
#     return stock_data

def get_sp500_tickers():
    # Fetch the S&P 500 tickers from Wikipedia
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    tickers = tables[0]['Symbol'].tolist()  # Get the first table and extract the 'Symbol' column
    return tickers

def get_stock_data(symbol):
    """Fetch stock data with retry logic."""
    retries = 5
    for attempt in range(retries):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Check if info is valid
            if not info or 'shortName' not in info:
                return None

            # Fetch historical data
            hist = stock.history(period="1d")
            current_price = hist['Close'].iloc[0] if not hist.empty else None

            return {
                'symbol': symbol,
                'name': info.get('shortName', 'N/A'),
                'price': current_price,
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A')
            }

        except Exception as e:
            logging.error(f"Error retrieving data for {symbol}: {e}")
            if "Too Many Requests" in str(e):
                logging.error("Rate limit hit, sleeping for 10 seconds...")
                time.sleep(10)  # Wait before retrying
            else:
                return None  # Return None for other errors

    return None  # Return None if all retries fail

def get_top_stocks(num_stocks=100, offset=0):
    global fetched_stocks, data_loading
    stock_data = []
    tickers = get_sp500_tickers()  # Get the S&P 500 tickers dynamically

    # Adjust the tickers list based on the offset
    #tickers = tickers[offset:offset + num_stocks]

    logging.info(f"Fetching {len(tickers)} tickers...")

    for symbol in tickers:
        data = get_stock_data(symbol)
        if data:
            stock_data.append(data)
        
        logging.info(f"Fetched data for {len(stock_data)} stocks.")

        # Rate limiting: sleep for a short time between requests
        #time.sleep(1)  # Sleep for 1 second between requests

    # Sort by market cap and return the stocks
    stock_data = sorted(stock_data, key=lambda x: x['market_cap'], reverse=True)

    logging.info(f"Fetching sorted {len(stock_data[offset:offset + num_stocks])} stocks...")

    fetched_stocks = stock_data

    data_loading = False
    # return stock_data[offset:offset + num_stocks]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)


