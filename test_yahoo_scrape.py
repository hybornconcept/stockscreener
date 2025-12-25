import requests
import pandas as pd
import io

def test_fetch_gainers():
    url = "https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=100"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print(f"Fetching {url}...")
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            # Use pandas to parse HTML tables
            # Yahoo gainers table usually has 'Symbol', 'Price', 'Change', '% Change' etc.
            dfs = pd.read_html(io.StringIO(response.text))
            
            print(f"Found {len(dfs)} tables.")
            
            for i, df in enumerate(dfs):
                print(f"Table {i} columns: {df.columns.tolist()}")
                if 'Symbol' in df.columns:
                    print(df[['Symbol', '% Change']].head())
                    return df['Symbol'].tolist()
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_fetch_gainers()
