import streamlit as st
import pandas as pd
import random
from src.data import get_top_gainers, fetch_market_data, enrich_with_float
from src.news import get_latest_headline
from config import USE_HISTORICAL_DATA, HISTORICAL_DATE
from utils.formatting import format_number

st.set_page_config(page_title="Warrior Stock Screener", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stDataFrame {font-size: 14px;}
    .block-container {max-width: 100%; padding-top: 1rem; padding-right: 2rem; padding-left: 2rem; padding-bottom: 3rem}
    /* Force text wrapping in dataframe cells */
    div[data-testid="stDataFrame"] div[role="gridcell"] {
        white-space: normal !important;
        overflow-wrap: anywhere !important;
        height: auto !important;
        min-height: 50px !important;
        line-height: 1.5 !important;
        display: block !important;
    }
    div[data-testid="stDataFrame"] div[role="gridcell"] > div {
        white-space: normal !important;
        overflow-wrap: anywhere !important;
        height: auto !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Franklyn Trading Stock Screener")

# Show warning if using historical data
if USE_HISTORICAL_DATA:
    st.warning(f"⚠️ **TESTING MODE**: Using historical data from {HISTORICAL_DATE} (Friday). Set `USE_HISTORICAL_DATA = False` in config.py for live data.")

# Sidebar settings
st.sidebar.header("Scanner Settings")




# Fetch Top Gainers (Scanning larger batch automatically)
n_tickers = 300
tickers_to_scan = get_top_gainers(count=n_tickers)  # This now calls get_top_gainers
total_available = len(tickers_to_scan)

st.sidebar.success(f"⚡ Market Scan Complete: Found {total_available} top gainers")

if st.button("🔄 Scan for Gainers") or "scan_results" not in st.session_state:
    with st.spinner(f"Fetching market data for {len(tickers_to_scan)} gainers..."):
        # 1. Fetch market data
        df_market = fetch_market_data(tickers_to_scan)
        
        if not df_market.empty:
            # 2. Enrich ALL with Float (User requirement: "float column is very important")
            df_market = enrich_with_float(df_market)
            
            # 3. Check Criteria (Conditions)
            from src.screener import check_basic_criteria, check_float_criteria
            
            # Basic criteria (Price, change, vol)
            basic_mask = check_basic_criteria(df_market)
            
            # Float criteria & Final "Conditions" column
            conditions = []
            final_matches = []
            
            for index, row in df_market.iterrows():
                is_basic = basic_mask[index]
                is_float = check_float_criteria(row)
                
                if is_basic and is_float:
                    conditions.append(True)
                    final_matches.append(row['Symbol'])
                else:
                    conditions.append(False)
                    
            df_market.insert(2, 'Conditions', conditions)
            
            # 4. Fetch Catalysts (News)
            # Optimization: Only fetch news for matches or top 10 if few matches
            # Fetching news for 300 stocks is too slow.
            targets_for_news = final_matches if final_matches else df_market['Symbol'].head(10).tolist()
            # Cap at 20 to prevent API timeouts
            targets_for_news = targets_for_news[:20]
            
            if targets_for_news:
                import concurrent.futures
                
                def fetch_catalyst_safe(sym):
                    try:
                        return get_latest_headline(sym)
                    except:
                        return {"summary": "Error", "url": None}

                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                     results = list(executor.map(fetch_catalyst_safe, targets_for_news))
                     
                news_map = dict(zip(targets_for_news, results))
                
                # Combine Summary + Link into one column
                def format_catalyst(sym):
                    res = news_map.get(sym)
                    if not res or not isinstance(res, dict): return ""
                    summary = res.get('summary', '')
                    return summary

                df_market['Catalyst'] = df_market['Symbol'].apply(format_catalyst)
                df_market['News Link'] = df_market['Symbol'].apply(lambda x: news_map.get(x, {}).get('url', None))
            else:
                df_market['Catalyst'] = ""
                df_market['News Link'] = None

            st.session_state['scan_results'] = df_market
        else:
            st.error("No market data fetched.")

# Display Results
if 'scan_results' in st.session_state:
    df_res = st.session_state['scan_results']
    
    # --- Sidebar Filters ---
    st.sidebar.divider()
    search_query = st.sidebar.text_input("🔍 Search Symbol or News", help="Filter table by text")
    
    # Filter Logic
    if search_query:
        # Case insensitive search in Symbol or Catalyst
        df_res = df_res[
            df_res['Symbol'].str.contains(search_query, case=False, na=False) | 
            df_res['Catalyst'].str.contains(search_query, case=False, na=False)
        ]

    # Show count
    st.subheader(f"Top Gainers ({len(df_res)} Found)")
    
    if not df_res.empty:
        # Reorder columns - Time first
        available_cols = df_res.columns.tolist()
        desired_cols = ['Time', 'Symbol', 'Conditions', 'Change %', 'Price', 'Avg Volume', 'Float', 'Rel Volume', 'Catalyst', 'News Link']
        
        display_cols = [c for c in desired_cols if c in available_cols]
        df_display = df_res[display_cols].copy()
        
        # Format large numbers
        if 'Avg Volume' in df_display.columns:
            df_display['Avg Volume'] = df_display['Avg Volume'].apply(format_number)
            
        # Display Table
        st.dataframe(
            df_display.style
            .format({
                'Price': '${:.2f}',
                'Change %': '{:.2f}',
                'Rel Volume': '{:.2f}'
            })
            .background_gradient(subset=['Change %'], cmap='RdYlGn', vmin=0)
            .background_gradient(subset=['Rel Volume'], cmap='Blues')
            ,
            height=1000, 
            column_config={
                "Conditions": st.column_config.CheckboxColumn(
                    "Conditions",
                    width="small",
                    help="Matches all criteria",
                ),
                "Catalyst": st.column_config.TextColumn(
                    "Catalyst (News)",
                    width="large",
                    help="News Summary"
                ),
                "News Link": st.column_config.LinkColumn(
                    "News Link",
                    display_text="Read More",
                    help="Click to read full story",
                    width="small"
                )
            },
            use_container_width=True
        )
    else:
        st.info("No stocks match the current filter.")

