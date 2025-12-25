# Testing Mode Configuration Guide

## Quick Toggle Between Historical and Live Data

### Using Historical Data (Testing Mode) - CURRENT SETTING ✓

Edit `config.py`:
```python
USE_HISTORICAL_DATA = True
HISTORICAL_DATE = "2024-12-20"  # Friday Dec 20, 2024
```

This mode:
- Fetches data from Friday, December 20, 2024
- Perfect for testing when market is closed
- Shows "2024-12-20 (Historical)" in the Time column
- Displays a warning banner at the top of the app

### Using Live Data (Production Mode)

Edit `config.py`:
```python
USE_HISTORICAL_DATA = False
HISTORICAL_DATE = "2024-12-20"  # This is ignored when USE_HISTORICAL_DATA = False
```

This mode:
- Fetches current real-time market data
- Shows actual trading time (e.g., "14:35:22")
- No warning banner
- Use this during market hours for live screening

## How to Switch

1. Open `config.py`
2. Change line 17: `USE_HISTORICAL_DATA = True` to `USE_HISTORICAL_DATA = False`
3. Save the file
4. Restart the Streamlit app (`streamlit run app.py`)

That's it! The app will automatically use the correct data source.

## Current Status

**Mode**: Historical Data Testing ✅
**Date**: Friday, December 20, 2024
**Purpose**: Testing the app when market is closed (weekend)

**Remember**: Switch back to `USE_HISTORICAL_DATA = False` when you want to use live data!
