from src.data import get_top_gainers, enrich_with_float
import pandas as pd
import time

print("Testing get_top_gainers...")
start = time.time()
tickers = get_top_gainers(count=50)
print(f"Got {len(tickers)} tickers in {time.time() - start:.2f}s")

if tickers:
    print(f"Sample: {tickers[:5]}")
    
    print("\nTesting enrich_with_float (Multithreaded)...")
    df = pd.DataFrame({'Symbol': tickers[:20]}) # Test with 20
    start = time.time()
    df = enrich_with_float(df)
    print(f"Enriched 20 tickers in {time.time() - start:.2f}s")
    print(df.head())
else:
    print("No tickers returned (Market might be closed or API issue)")
