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
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import yfinance
import yfinance as yf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
            login_user(user)
            return redirect(url_for('index'))
        flash('Login failed, check your credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.')
    return redirect(url_for('login'))

# Home route
@app.route('/')
@login_required
def index():
    stocks = get_top_50_stocks()  # Get top 50 stock stats
    return render_template('index.html', stocks=stocks)

# Route for stock details (graphs and information)
@app.route('/stock/<symbol>')
@login_required
def stock_details(symbol):
    stock = yfinance.Ticker(symbol)
    hist = stock.history(period="5y")
    return render_template('stock_details.html', stock=stock, hist=hist)

# Helper function (unchanged)
def get_top_50_stocks():
    top_50_stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'JNJ', 'WMT', 
          'PG', 'MA', 'DIS', 'NFLX', 'HD', 'PFE', 'KO', 'PEP', 'MRK',         'XOM', 'BAC', 'CVX', 'NKE', 'CSCO', 'ABT', 'TMO', 'LLY', 'ORCL', 'UNH',
        'BABA', 'CRM', 'COST', 'QCOM', 'INTC', 'MDT', 'MCD', 'TMUS', 'UPS', 'HON',
        'IBM', 'AMD', 'DHR', 'TXN', 'NEE', 'SPGI', 'SBUX', 'BLK', 'GS', 'LOW']  # Same stock symbols as before
    stock_data = []

    for symbol in top_50_stocks:
        # stock = YieldFrom.Ticker(symbol)
        stock = yf.Ticker(symbol)
        info = stock.info
        hist = stock.history(period="1d")
        current_price = hist['Close'].iloc[0] if not hist.empty else None

        stock_data.append({
            'symbol': symbol,
            'name': info.get('shortName', 'N/A'),
            'price': current_price,
            'market_cap': info.get('marketCap', 'N/A'),
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'dividend_yield': info.get('dividendYield', 'N/A')
        })
    return stock_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

