from config import MIN_PRICE, MAX_PRICE, MIN_DAY_CHANGE_PCT, MIN_RELATIVE_VOLUME

def filter_stocks(df):
    """
    Applies Warrior Trading criteria to the dataframe.
    """
    if df.empty:
        return df

    # 1. Price Range ($1.00 - $20.00)
    df_filtered = df[(df['Price'] >= MIN_PRICE) & (df['Price'] <= MAX_PRICE)].copy()
    
    # 2. Percentage Change (>= 10%)
    df_filtered = df_filtered[df_filtered['Change %'] >= MIN_DAY_CHANGE_PCT]
    
    # 3. Relative Volume (>= 5x)
    df_filtered = df_filtered[df_filtered['Rel Volume'] >= MIN_RELATIVE_VOLUME]
    
    return df_filtered
