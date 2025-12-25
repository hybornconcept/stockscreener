import pandas as pd
from src.screener import check_basic_criteria, check_float_criteria
from config import MIN_PRICE, MAX_FLOAT

def test_screener_logic():
    print("Testing Screener Logic...")
    
    # Mock Data
    data = {
        'Symbol': ['A', 'B', 'C'],
        'Price': [5.0, 150.0, 2.5], # B fails price (max 100)
        'Change %': [10.0, 5.0, 2.0], # C fails change (min 5.0)
        'Rel Volume': [3.0, 5.0, 1.0], # C fails rel vol (min 2.0)
        'Float': ['10M', 'N/A', '60M'] # C fails float (max 50M)
    }
    df = pd.DataFrame(data)
    
    print("\nDataFrame:")
    print(df)
    
    # 1. Basic Criteria
    print("\nChecking Basic Criteria...")
    mask = check_basic_criteria(df)
    print(mask)
    # Expect: A=True, B=False (Price>100), C=False (Change<5, RelVol<2)
    
    # 2. Float Criteria
    print("\nChecking Float Criteria (Row A)...")
    res_a = check_float_criteria(df.iloc[0])
    print(f"Row A (10M <= {MAX_FLOAT}): {res_a}") # True
    
    print("Checking Float Criteria (Row C)...")
    res_c = check_float_criteria(df.iloc[2])
    print(f"Row C (60M <= {MAX_FLOAT}): {res_c}") # False

if __name__ == "__main__":
    test_screener_logic()
