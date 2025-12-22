# 🛡️ Warrior Trading Stock Screener

A powerful, real-time stock screening application built with Streamlit that identifies high-momentum trading opportunities based on Warrior Trading criteria. This tool helps day traders and swing traders discover stocks with significant price movements, high relative volume, and relevant market catalysts.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Screening Criteria](#screening-criteria)
- [How It Works](#how-it-works)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## ✨ Features

- **Real-time Market Data**: Fetches live stock data using Yahoo Finance API
- **Warrior Trading Criteria**: Filters stocks based on proven day trading parameters
- **Catalyst Detection**: Automatically fetches the latest news headlines for each candidate stock
- **Float Analysis**: Enriches results with share float data for better trade planning
- **Interactive Dashboard**: Beautiful Streamlit interface with color-coded metrics
- **Customizable Scanning**: Adjust sample size and reshuffle tickers on demand
- **Relative Volume Calculation**: Identifies unusual trading activity
- **Batch Processing**: Efficiently scans hundreds of tickers simultaneously
- **Google Colab Support**: Includes Jupyter notebook for GPU-accelerated scanning

## 🎯 Demo

The screener displays top gainers with the following information:
- **Change %**: Percentage price change (color-coded)
- **Symbol**: Stock ticker
- **Price**: Current stock price
- **Volume**: Trading volume (formatted for readability)
- **Float**: Number of shares available for trading
- **Rel Volume**: Relative volume compared to average
- **Time**: Last update timestamp
- **Catalyst**: Latest news headline or market event

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection for real-time data

### Step 1: Clone the Repository

```bash
git clone https://github.com/hybornconcept/stockscreener.git
cd stockscreener
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 💻 Usage

### Running the Streamlit App

1. **Launch the app**:
   ```bash
   streamlit run app.py
   ```

2. **Adjust Settings** (in sidebar):
   - Use the slider to change the sample size (10-500 tickers)
   - Click "Shuffle Tickers" to scan a new random batch
   - Click "Refresh Data" to update market data

3. **View Results**:
   - Top section shows filtered stocks meeting all criteria
   - Bottom section displays all scanned stocks sorted by performance

### Running the Batch Script (Windows)

For quick scanning without the web interface:

```bash
run_screener.bat
```

### Using Google Colab

Open `StockScreener_Colab.ipynb` in Google Colab for cloud-based execution with GPU acceleration.

## ⚙️ Configuration

Edit `config.py` to customize screening parameters:

```python
# Stock Selection Criteria
MIN_PRICE = 2.00              # Minimum stock price ($)
MAX_PRICE = 50.00             # Maximum stock price ($)
MIN_DAY_CHANGE_PCT = 10.0     # Minimum daily change (%)
MIN_RELATIVE_VOLUME = 5.0     # Minimum relative volume multiplier

# Application Settings
NUMBER_OF_TICKERS_TO_SCAN = 100  # Default number of tickers to scan
```

### Customization Tips

- **For Penny Stocks**: Lower `MIN_PRICE` to 0.50 and `MAX_PRICE` to 5.00
- **For Large Caps**: Increase `MIN_PRICE` to 50.00 and `MAX_PRICE` to 500.00
- **For Volatile Markets**: Increase `MIN_DAY_CHANGE_PCT` to 20.0+
- **For High Volume**: Increase `MIN_RELATIVE_VOLUME` to 10.0+

## 📁 Project Structure

```
stockscreener/
│
├── app.py                          # Main Streamlit application
├── main.py                         # Standalone earnings data fetcher
├── config.py                       # Configuration parameters
├── requirements.txt                # Python dependencies
├── run_screener.bat               # Windows batch script
├── read_pdf.py                    # PDF parsing utility
│
├── src/
│   ├── data.py                    # Data fetching and processing
│   ├── screener.py                # Stock filtering logic
│   └── news.py                    # News/catalyst fetching
│
├── utils/
│   └── formatting.py              # Number formatting utilities
│
├── StockScreener_Colab.ipynb      # Google Colab notebook
└── Warrior Trading - Stock Selection.pdf  # Reference documentation
```

## 🎯 Screening Criteria

The screener applies the following Warrior Trading criteria:

### 1. Price Range
- **Minimum**: $2.00
- **Maximum**: $50.00
- **Rationale**: Focuses on stocks with sufficient liquidity while avoiding extreme penny stocks

### 2. Daily Change
- **Minimum**: 10% gain
- **Rationale**: Identifies stocks with significant momentum and trader interest

### 3. Relative Volume
- **Minimum**: 5x average volume
- **Rationale**: Ensures unusual trading activity indicating potential catalysts

### 4. Float Analysis
- Enriches results with share float data
- Helps identify stocks with potential for explosive moves

### 5. Catalyst Detection
- Fetches latest news headlines
- Provides context for price movements

## 🔧 How It Works

### Data Flow

1. **Ticker Selection**
   - Fetches comprehensive ticker list from GitHub repository
   - Randomly samples specified number of tickers
   - Allows reshuffling for new batches

2. **Market Data Fetching**
   ```python
   # Uses yfinance to get real-time data
   - Current price
   - Daily change percentage
   - Volume metrics
   - Historical averages
   ```

3. **Filtering Process**
   ```python
   # Applies sequential filters
   1. Price range filter
   2. Percentage change filter
   3. Relative volume filter
   ```

4. **Enrichment**
   ```python
   # Adds additional data
   - Share float from Yahoo Finance
   - Latest news headlines
   - Formatted timestamps
   ```

5. **Display**
   - Color-coded metrics
   - Sortable columns
   - Gradient backgrounds for quick visual analysis

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)**: Web application framework
- **[yfinance](https://github.com/ranaroussi/yfinance)**: Yahoo Finance API wrapper
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation and analysis
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)**: Web scraping for news
- **[Requests](https://requests.readthedocs.io/)**: HTTP library for API calls
- **[lxml](https://lxml.de/)**: XML/HTML processing

## 📊 Performance Optimization

- **Caching**: Streamlit's `@st.cache_data` for ticker lists
- **Batch Processing**: Efficient concurrent data fetching
- **Session State**: Maintains data between interactions
- **Lazy Loading**: Only enriches filtered results

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Ideas for Contributions

- Add technical indicators (RSI, MACD, etc.)
- Implement backtesting functionality
- Add email/SMS alerts for matches
- Create mobile-responsive design
- Add database storage for historical tracking
- Implement machine learning predictions

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT**: This tool is for educational and informational purposes only. It is NOT financial advice.

- **No Investment Advice**: The information provided does not constitute investment advice, financial advice, trading advice, or any other sort of advice.
- **Do Your Own Research**: Always conduct your own research and consult with a licensed financial advisor before making investment decisions.
- **Risk Warning**: Trading stocks involves substantial risk of loss and is not suitable for every investor.
- **No Guarantees**: Past performance is not indicative of future results. The screener's criteria do not guarantee profitable trades.
- **Data Accuracy**: While we strive for accuracy, real-time data may have delays or errors. Always verify information before trading.

## 📞 Support

For questions, issues, or suggestions:

- **GitHub Issues**: [Create an issue](https://github.com/hybornconcept/stockscreener/issues)
- **Email**: hyborninc@gmail.com

## 🙏 Acknowledgments

- **Warrior Trading**: For the screening methodology and educational content
- **Yahoo Finance**: For providing free market data API
- **Streamlit Community**: For the excellent framework and documentation

## 📈 Roadmap

- [ ] Add technical analysis indicators
- [ ] Implement real-time alerts
- [ ] Create historical performance tracking
- [ ] Add options flow data
- [ ] Implement dark pool activity monitoring
- [ ] Add sector/industry filtering
- [ ] Create mobile app version
- [ ] Add paper trading simulation

---

**Made with ❤️ by [hyborn](https://github.com/hybornconcept)**

**⭐ Star this repo if you find it useful!**