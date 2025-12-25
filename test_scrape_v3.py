from src.data import get_top_gainers
import time

print("Testing get_top_gainers (New Scraping Implementation)...")
start = time.time()
tickers = get_top_gainers(count=50)
print(f"Got {len(tickers)} tickers in {time.time() - start:.2f}s")
if tickers:
    print(f"Tickers found: {tickers[:10]}...")
else:
    print("No tickers found (Check network or layout changes)")
