import yfinance as yf
import pandas as pd
import requests
import random
import streamlit as st
from datetime import datetime
from config import NUMBER_OF_TICKERS_TO_SCAN, TICKER_SOURCE_URL
from utils.formatting import format_number

@st.cache_data(ttl=3600)  # Cache ticker list for 1 hour
def get_random_tickers(n=NUMBER_OF_TICKERS_TO_SCAN):
    """Fetches a list of US tickers and returns a random sample."""
    try:
        response = requests.get(TICKER_SOURCE_URL)
        response.raise_for_status()
        tickers = response.text.splitlines()
        tickers = [t.strip() for t in tickers if t.strip()]
        # We grab a larger pool initially so we can sample from it
        return tickers
    except Exception as e:
        print(f"Error fetching ticker list: {e}")
        return ["AAPL", "MSFT", "AMZN", "NVDA", "TSLA", "GME", "AMC", "BB", "PLTR", "SOFI"]

@st.cache_data(ttl=60) # Cache market data for 60 seconds
def fetch_market_data(tickers):
    """
    Fetches current market data for the given tickers using yfinance.
    """
    data = []
    try:
        # Fetch 1mo history
        history = yf.download(tickers, period="1mo", group_by='ticker', progress=False, threads=True, auto_adjust=True)
        
        current_time = datetime.now().strftime("%H:%M:%S")

        for ticker in tickers:
            try:
                if len(tickers) == 1:
                    df_ticker = history
                else:
                    if ticker not in history.columns.levels[0]:
                        continue
                    df_ticker = history[ticker]
                
                if df_ticker.empty:
                    continue
                
                latest = df_ticker.iloc[-1]
                prev = df_ticker.iloc[-2] if len(df_ticker) > 1 else latest
                
                price = latest['Close']
                prev_close = prev['Close']
                volume = latest['Volume']
                
                change_pct = ((price - prev_close) / prev_close) * 100
                avg_volume = df_ticker['Volume'].mean()
                rel_vol = volume / avg_volume if avg_volume > 0 else 0
                
                data.append({
                    'Symbol': ticker,
                    'Time': current_time,
                    'Price': float(price),
                    'Change %': float(change_pct),
                    'Volume': int(volume),
                    'Avg Volume': int(avg_volume),
                    'Rel Volume': float(rel_vol),
                    'Float': 'N/A' # Placeholder, will enrich later
                })
                
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"Batch download error: {e}")
        
    return pd.DataFrame(data)

def enrich_with_float(df):
    """
    Fetches Float data for the filtered DataFrame. 
    """
    floats = []
    for symbol in df['Symbol']:
        try:
            # fast_info is generally faster and contains float_shares
            fast_info = yf.Ticker(symbol).fast_info
            # Check safely
            if 'float_shares' in fast_info:
                f = fast_info['float_shares']
            else:
                # Fallback to .info (slower)
                f = yf.Ticker(symbol).info.get('floatShares', None)
            
            floats.append(format_number(f) if f else 'N/A')
        except:
            floats.append('N/A')
    df['Float'] = floats
    return df
