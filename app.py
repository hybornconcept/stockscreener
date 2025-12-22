import streamlit as st
import pandas as pd
import random
from src.data import get_random_tickers, fetch_market_data, enrich_with_float
from src.screener import filter_stocks
from src.news import get_latest_headline
from config import NUMBER_OF_TICKERS_TO_SCAN
from utils.formatting import format_number

st.set_page_config(page_title="Warrior Stock Screener", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stDataFrame {font-size: 14px;}
    .block-container {max-width: 100%; padding-top: 1rem; padding-right: 2rem; padding-left: 2rem; padding-bottom: 3rem}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Warrior Trading Stock Screener")

# Sidebar settings
st.sidebar.header("Scanner Settings")
n_tickers = st.sidebar.slider("Sample Size (random tickers)", 10, 500, NUMBER_OF_TICKERS_TO_SCAN)

# Initialize session state for tickers
if 'tickers' not in st.session_state:
    all_tickers = get_random_tickers(10000) # Fetch all/many
    st.session_state['tickers'] = random.sample(all_tickers, n_tickers)

# Helper to reshuffle
def shuffle_tickers():
    all_tickers = get_random_tickers(10000)
    st.session_state['tickers'] = random.sample(all_tickers, n_tickers)

if st.sidebar.button("Shuffle Tickers"):
    shuffle_tickers()
    st.rerun()

if st.button("Refresh Data") or "scan_results" not in st.session_state:
    with st.spinner(f"Scanning {n_tickers} tickers..."):
        # 1. Use stored tickers
        tickers = st.session_state['tickers']
        
        # 2. Fetch Data (Cached by Streamlit for ttl=60s)
        # We need to slice in case slider changed
        if len(tickers) < n_tickers:
             shuffle_tickers()
             tickers = st.session_state['tickers']
        
        current_batch = tickers[:n_tickers]
        df_market = fetch_market_data(current_batch)
        
        if not df_market.empty:
            st.session_state['scan_results'] = df_market
            
            # 2. Filter
            filtered_df = filter_stocks(df_market)
            
            # 3. Enrich Candidates (Float + Catalyst)
            if not filtered_df.empty:
                filtered_df = enrich_with_float(filtered_df)
                
                # Fetch Catalysts
                catalysts = []
                for sym in filtered_df['Symbol']:
                    catalysts.append(get_latest_headline(sym))
                filtered_df['Catalyst'] = catalysts
                
            st.session_state['filtered_results'] = filtered_df
        else:
            st.error("No market data fetched.")

# Display Results
if 'filtered_results' in st.session_state:
    df_res = st.session_state['filtered_results']
    df_all = st.session_state.get('scan_results', pd.DataFrame())
    
    if not df_res.empty:
        st.subheader(f"Top Gainers ({len(df_res)} Matches)")
        # Reorder columns to match request roughly
        # Change %, Symbol, Price, Volume, Float, Rel Volume, Time, Catalyst
        display_cols = ['Change %', 'Symbol', 'Price', 'Volume', 'Float', 'Rel Volume', 'Time', 'Catalyst']
        df_display = df_res[display_cols].copy()
        
        # Format large numbers for display (Volume is int, change to string formatted)
        df_display['Volume'] = df_display['Volume'].apply(format_number)
        
        # Styling
        st.dataframe(
            df_display.style
            .format({
                'Price': '${:.2f}',
                'Change %': '{:.2f}',
                'Rel Volume': '{:.2f}'
            })
            .background_gradient(subset=['Change %'], cmap='RdYlGn', vmin=0)
            .background_gradient(subset=['Rel Volume'], cmap='Blues')
            .set_properties(**{'text-align': 'center'})
        , use_container_width=True, height=1000)
    else:
        st.warning("No matches found in this batch. Try 'Shuffle Tickers' to scan a new group or lower the criteria.")
        
    st.divider()
    st.subheader("Market Scan Preview (All Loaded Tickers)")
    st.dataframe(
        df_all
        .sort_values('Change %', ascending=False)
        .head(50)
        .style.format({'Change %': '{:.2f}', 'Price': '${:.2f}', 'Rel Volume': '{:.2f}'})
        .background_gradient(subset=['Change %'], cmap='RdYlGn'),
        use_container_width=True
    )
