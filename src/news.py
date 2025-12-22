import yfinance as yf

def get_catalysts(symbol):
    """
    Fetches latest news for a specific stock symbol to identify catalysts.
    """
    try:
        ticker = yf.Ticker(symbol)
        news_items = ticker.news
        
        formatted_news = []
        for item in news_items:
            formatted_news.append({
                'Title': item.get('title'),
                'Publisher': item.get('publisher'),
                'Link': item.get('link'),
                'Time': item.get('providerPublishTime')
            })
        return formatted_news
    except Exception as e:
        return []

def get_latest_headline(symbol):
    """
    Fetches the latest news headline as a catalyst summary (approx < 50 words).
    """
    try:
        news = get_catalysts(symbol)
        if news:
            latest = news[0]
            # Create a summary string
            summary = f"{latest['Title']} ({latest['Publisher']})"
            # Truncate if too long (rough word count)
            words = summary.split()
            if len(words) > 50:
                summary = " ".join(words[:50]) + "..."
            return summary
    except Exception as e:
        # print(f"News error for {symbol}: {e}")
        pass
    return "No recent news found"
