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

def get_latest_headline(symbol, max_words=50):
    """
    Fetches the latest news headline as a catalyst summary (max 50 words).
    Returns a concise summary of the most recent news for the stock.
    """
    try:
        ticker = yf.Ticker(symbol)
        news_items = ticker.news
        
        if news_items and len(news_items) > 0:
            latest = news_items[0]
            title = latest.get('title', '')
            
            # Create a clean summary
            words = title.split()
            if len(words) > max_words:
                summary = " ".join(words[:max_words]) + "..."
            else:
                summary = title
                
            return summary if summary else "No recent news"
        else:
            return "No recent news"
            
    except Exception as e:
        return "No recent news"
