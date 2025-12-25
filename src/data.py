import yfinance as yf
import pandas as pd
import requests
import random
import streamlit as st
import concurrent.futures
import logging
import io
from datetime import datetime, timedelta
from config import USE_HISTORICAL_DATA, HISTORICAL_DATE, TICKER_SOURCE_URL
from utils.formatting import format_number

# Silence yfinance loggers
logging.getLogger('yfinance').setLevel(logging.CRITICAL)
logging.getLogger('yahoo_fin').setLevel(logging.CRITICAL)

@st.cache_data(ttl=86400)
def get_all_tickers():
    """
    Deprecated: No longer needed for the direct gainers scan, but kept for fallback/historical modes.
    """
    try:
        response = requests.get(TICKER_SOURCE_URL)
        if response.status_code == 200:
            lines = response.text.splitlines()
            tickers = [t.strip() for t in lines if t.strip().isalpha() and len(t.strip()) <= 4]
            return tickers
    except Exception as e:
        pass
    return []

@st.cache_data(ttl=60)
def get_top_gainers(count=100):
    """
    Fetches the top gainers directly from Yahoo Finance's 'Day Gainers' page.
    This is much faster and more accurate than scanning random tickers.
    """
    url = "https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=100"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    symbols = []
    
    try:
        # 1. Scraping Yahoo Gainers
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                # pandas use lxml or beautifulsoup4 to parse tables
                dfs = pd.read_html(io.StringIO(response.text))
                
                # The gainers table is usually the first one
                if dfs:
                    df = dfs[0]
                    # Check for symbol column
                    if 'Symbol' in df.columns:
                        # Clean symbols (remove anything with odd chars if needed, though usually fine)
                        raw_symbols = df['Symbol'].tolist()
                        # Filter out NaNs and ensure strings
                        symbols = [str(s).strip() for s in raw_symbols if isinstance(s, str) or (pd.notna(s) and str(s).strip())]
                        
                        # Return requested count
                        return symbols[:count]
            except ValueError as e:
                print(f"Error parsing HTML table: {e}")
                
    except Exception as e:
        print(f"Error fetching gainers from Yahoo: {e}")

    # 2. Fallback Mechanism
    # If scraping fails, we fall back to the old method of scanning a subset of known active tickers
    print("Fallback: Scanning known tickers...")
    fallback_tickers = [
        'TSLA', 'NVDA', 'AMD', 'GME', 'AMC', 'MARA', 'COIN', 'PLTR', 'SOFI', 'AAPL', 
        'MSFT', 'AMZN', 'GOOGL', 'META', 'NFLX', 'RIVN', 'LCID', 'NIO', 'BABA'
    ]
    # Add some random ones if we can
    all_t = get_all_tickers()
    if all_t:
        random.shuffle(all_t)
        fallback_tickers.extend(all_t[:500]) # Scan 500 randoms
        
    return fallback_tickers

# Alias
get_comprehensive_ticker_list = get_top_gainers

@st.cache_data(ttl=60)
def fetch_market_data(tickers):
    """
    Fetches market data (Price, Change, Vol) for a list of tickers.
    """
    data_list = []
    
    if not tickers:
        return pd.DataFrame()
        
    try:
        if USE_HISTORICAL_DATA:
            target_date = datetime.strptime(HISTORICAL_DATE, "%Y-%m-%d")
            start_date = (target_date - timedelta(days=10)).strftime("%Y-%m-%d")
            end_date = (target_date + timedelta(days=1)).strftime("%Y-%m-%d")
            
            # Fetch historical
            history = yf.download(tickers, start=start_date, end=end_date, 
                                group_by='ticker', progress=False, threads=True, auto_adjust=True)
            display_time = f"{HISTORICAL_DATE} (Historical)"
        else:
            # Fetch Live
            # period='5d' is safe to get previous close info
            history = yf.download(tickers, period="5d", group_by='ticker', 
                                progress=False, threads=True, auto_adjust=True)
            # Format: M/D/YYYY H:MM AM/PM (e.g., 9/12/2017 9:11 AM)
            # Windows uses # instead of - to remove leading zeros
            display_time = datetime.now().strftime("%#m/%#d/%Y %#I:%M %p")

        if history.empty:
            return pd.DataFrame()

        # Handle Single Ticker vs Multi Ticker dataframe structures
        valid_tickers = [t for t in tickers if t in history.columns.levels[0]] if isinstance(history.columns, pd.MultiIndex) else tickers

        # If only one ticker was passed and returned, history columns are just the fields (Open, Close...)
        if len(tickers) == 1 and not isinstance(history.columns, pd.MultiIndex):
             # Wrap it to treat consistently? Or just handle one case.
             # Easier to just re-download as list? No.
             # Lets valid_tickers = [tickers[0]]
             # But fetching df[ticker] will fail.
             pass 

        for ticker in tickers:
            try:
                # Extract ticker dataframe
                if isinstance(history.columns, pd.MultiIndex):
                    if ticker not in history.columns.levels[0]:
                        continue
                    df_ticker = history[ticker]
                else:
                    # Single ticker result
                    if ticker != tickers[0]: continue
                    df_ticker = history
                
                if df_ticker.empty:
                    continue
                    
                # Ensure we have enough data
                if len(df_ticker) < 1: continue
                
                latest = df_ticker.iloc[-1]
                
                # Get Prev Close for calculation
                if len(df_ticker) > 1:
                    prev_close = df_ticker.iloc[-2]['Close']
                else:
                    # If only 1 day of data (e.g. IPO today), define prev_close as Open
                    prev_close = latest['Open']
                
                price = latest['Close']
                volume = latest['Volume']
                
                # Handle potential Series objects
                if isinstance(price, pd.Series): 
                    price = price.iloc[0]
                if isinstance(volume, pd.Series): 
                    volume = volume.iloc[0]
                if isinstance(prev_close, pd.Series): 
                    prev_close = prev_close.iloc[0]
                
                if prev_close == 0: continue
                
                change_pct = ((price - prev_close) / prev_close) * 100
                
                # Append raw data
                data_list.append({
                    'Time': display_time,
                    'Symbol': ticker,
                    'Price': float(price),
                    'Change %': float(change_pct),
                    'Avg Volume': int(df_ticker['Volume'].mean()),
                    'Rel Volume': float(volume / df_ticker['Volume'].mean()) if df_ticker['Volume'].mean() > 0 else 0.0,
                    'Float': 'N/A'
                })
            except Exception as e:
                # Print specific error for debugging
                print(f"Error processing {ticker}: {e}")
                continue
                
    except Exception as e:
        print(f"Data fetch error: {e}")
        
    return pd.DataFrame(data_list)

def get_single_float(symbol):
    """Helper function to fetch float for a single ticker"""
    try:
        ticker = yf.Ticker(symbol)
        float_shares = None
        
        # Method 1: Fast Info
        try:
            fast_info = ticker.fast_info
            if hasattr(fast_info, 'shares') and hasattr(fast_info, 'shares_outstanding'):
                 float_shares = getattr(fast_info, 'shares', None)
        except:
            pass
        
        # Method 2: Info dict
        if float_shares is None:
            try:
                info = ticker.info
                float_shares = info.get('floatShares') or info.get('sharesOutstanding')
            except:
                pass
        
        if float_shares and float_shares > 0:
            return format_number(float_shares)
    except:
        pass
    return 'N/A'

def enrich_with_float(df):
    """
    Fetches Float data for the filtered DataFrame using Multithreading.
    """
    if df.empty:
        return df

    symbols = df['Symbol'].tolist()
    floats = []
    
    # Threaded enrichment
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        floats = list(executor.map(get_single_float, symbols))
            
    df['Float'] = floats
    return df
