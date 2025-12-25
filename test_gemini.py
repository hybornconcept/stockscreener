"""
Quick test script for Gemini AI news summarization
"""
from src.news import get_latest_headline, summarize_with_gemini

# Test with a popular stock
test_symbol = "AAPL"

print(f"Testing Gemini AI news summarization for {test_symbol}...")
print("=" * 60)

catalyst = get_latest_headline(test_symbol)
print(f"\nCatalyst Summary:\n{catalyst}")
print("\n" + "=" * 60)
print("\n✓ Test completed!")
print("If you see a summarized news above, Gemini integration is working!")
