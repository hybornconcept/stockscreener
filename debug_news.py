import requests
import json
from config import OPENROUTER_API_KEY

def test_tickertick(symbol):
    print(f"Testing TickerTick for {symbol}...")
    url = f"https://api.tickertick.com/feed?q=z:{symbol}&n=10"
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            stories = data.get('stories', [])
            print(f"Found {len(stories)} stories.")
            for i, story in enumerate(stories[:3]):
                print(f"Story {i+1}: {story.get('title')}")
                print(f"URL: {story.get('url')}")
            return stories
        else:
            print(f"Error content: {response.text}")
            return []
    except Exception as e:
        print(f"Exception: {e}")
        return []

def test_llm(text):
    print("\nTesting LLM...")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501", 
        "X-Title": "StockScreener", 
    }
    
    prompt = f"Summarize this: {text[:500]}"
    
    data = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=20)
        print(f"LLM Status Code: {response.status_code}")
        if response.status_code == 200:
            print("LLM Response received.")
            print(response.json()['choices'][0]['message']['content'])
        else:
            print(f"LLM Error: {response.text}")
    except Exception as e:
        print(f"LLM Exception: {e}")

if __name__ == "__main__":
    stories = test_tickertick("AAPL")
    if stories:
        combined_text = " ".join([s.get('description', '') for s in stories])
        test_llm(combined_text)
