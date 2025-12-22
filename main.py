import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "AMZN", "NVDA", "TSLA"]
all_earnings = []

for symbol in tickers:
    ticker_obj = yf.Ticker(symbol)
    
    # Get the earnings history table directly
    # This includes EPS Estimate, Reported, and Surprise %
    try:
        history = ticker_obj.earnings_dates
        if history is not None:
            history = history.reset_index()
            history['Symbol'] = symbol
            all_earnings.append(history)
    except Exception as e:
        print(f"Could not fetch data for {symbol}: {e}")

# Combine into one dataframe
if all_earnings:
    df = pd.concat(all_earnings)
    print(df.head())
else:
    print("No earnings data found.")
