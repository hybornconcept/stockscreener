import datetime

# Configuration for Warrior Trading Criteria and Application Settings

# Stock Selection Criteria
MIN_PRICE = 2.00
MAX_PRICE = 500.00
MIN_DAY_CHANGE_PCT = 5.0
MIN_RELATIVE_VOLUME = 0.5
MAX_FLOAT = 50_000_000  # 50 million


# Application Settings
TICKER_SOURCE_URL = "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/all/all_tickers.txt"

# OpenRouter API Configuration
OPENROUTER_API_KEY = "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"
SITE_URL = "http://localhost:8501" # Optional. Site URL for rankings on openrouter.ai.
SITE_NAME = "StockScreener" # Optional. Site title for rankings on openrouter.ai.

# Testing Mode (set to False for live market data)
USE_HISTORICAL_DATA = False
HISTORICAL_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

FMP_API_KEY = "8KkwuSIg4MBkJCL7CVAoo4EuhmqRZWJX"
