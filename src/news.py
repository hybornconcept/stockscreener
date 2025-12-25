import requests
import json
import yfinance as yf
from config import OPENROUTER_API_KEY, SITE_URL, SITE_NAME

def get_company_name(symbol):
    """
    Fetches the full company name for a ticker symbol.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Try different fields for company name
        company_name = info.get('longName') or info.get('shortName') or symbol
        return company_name
    except:
        return symbol

def summarize_with_glm(news_text, symbol, company_name):
    """
    Uses GLM-4.5-Air via OpenRouter to create a concise summary.
    Constraints: 40-50 words.
    """
    if not news_text:
        return None

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_NAME,
    }

    # Prompt engineering for the constraints
    prompt = f"""Summarize the following news for {company_name} ({symbol}).
    
    News Content:
    {news_text}
    
    Instructions:
    1. The summary MUST be between 40 and 50 words long. This is a STRICT requirement.
    2. Focus on the main catalyst or reason for stock movement.
    3. Do not include introductory phrases like "The news reports...". just the summary.
    4. Return ONLY the summary text.
    """

    data = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                summary = result['choices'][0]['message']['content'].strip()
                return summary
            else:
                return None
        else:
            print(f"GLM API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"GLM Exception for {symbol}: {e}")
        return None

    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return {"summary": "Error fetching news", "url": None}

def get_latest_headline(symbol):
    """
    Fetches the latest news using TickerTick API and summarizes it using GLM-4.5-Air.
    Returns a dictionary: {'summary': str, 'url': str}
    """
    try:
        company_name = get_company_name(symbol)
        
        # TickerTick API call
        # q=z:{symbol} filters for the specific ticker
        # n=2 as requested
        url = f"https://api.tickertick.com/feed?q=z:{symbol}&n=2"
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            stories = data.get('stories', [])
            
            if stories:
                # Sort by time property to ensure latest
                # TickerTick 'time' field is a timestamp (milliseconds usually).
                # Sort descending.
                stories.sort(key=lambda x: x.get('time', 0), reverse=True)
                
                # Get the most latest news
                latest_story = stories[0]
                
                title = latest_story.get('title', '')
                description = latest_story.get('description', '')
                story_url = latest_story.get('url', None)
                
                full_text = f"{title}. {description}"
                
                if not full_text.strip():
                     return {"summary": "No distinct news found", "url": story_url}

                # Get AI summary
                ai_summary = summarize_with_glm(full_text, symbol, company_name)
                
                if ai_summary:
                    # Final check on word count (approximate)
                    # We trust the LLM mostly, but if it fails significantly we could fallback, 
                    # but user specifically asked for this LLM configuration.
                    return {"summary": ai_summary, "url": story_url}
                else:
                    return {"summary": title, "url": story_url} # Fallback to title
            else:
                return {"summary": "No recent news found", "url": None}
        else:
             return {"summary": "News API Error", "url": None}
             
    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return {"summary": "Error fetching news", "url": None}
