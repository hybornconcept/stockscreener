import pandas as pd
from config import MIN_PRICE, MAX_PRICE, MIN_DAY_CHANGE_PCT, MIN_RELATIVE_VOLUME, MAX_FLOAT

def check_basic_criteria(df):
    """
    Checks Price, Change %, and Volume criteria.
    Returns a boolean Series indicating matches.
    """
    if df.empty:
        return pd.Series(dtype=bool)

    mask = (
        (df['Price'] >= MIN_PRICE) & 
        (df['Price'] <= MAX_PRICE) &
        (df['Change %'] >= MIN_DAY_CHANGE_PCT) &
        (df['Rel Volume'] >= MIN_RELATIVE_VOLUME)
    )
    return mask

def check_float_criteria(row):
    """
    Checks if Float meets criteria.
    Assumes 'Float' column exists and is populated.
    """
    val = row.get('Float')
    if not val or val == 'N/A':
        return False
        
    # Parse float string (e.g. 15.5M) or number
    try:
        if isinstance(val, (int, float)):
            f_val = val
        else:
            s_val = str(val).replace(',', '').upper()
            if 'K' in s_val:
                f_val = float(s_val.replace('K', '')) * 1_000
            elif 'M' in s_val:
                f_val = float(s_val.replace('M', '')) * 1_000_000
            elif 'B' in s_val:
                f_val = float(s_val.replace('B', '')) * 1_000_000_000
            else:
                f_val = float(s_val)
                
        return f_val <= MAX_FLOAT
    except:
        return False
