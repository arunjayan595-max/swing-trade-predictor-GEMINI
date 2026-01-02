import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import logging
import random

logger = logging.getLogger(__name__)

# Basic keywords for sentiment scoring
NEGATIVE_KEYWORDS = ["fraud", "scam", "investigation", "resignation", "lawsuit", "crash", "plunge", "loss"]
POSITIVE_KEYWORDS = ["profit", "surge", "growth", "record", "acquisition", "dividend", "bonus", "win"]
CAUTION_KEYWORDS = ["earnings", "result", "quarterly"]

def fetch_rss_feed(url: str):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
        return None
    except Exception as e:
        logger.error(f"Error fetching RSS: {e}")
        return None

def analyze_headline(text: str) -> dict:
    """Analyze a single headline for sentiment."""
    text_lower = text.lower()
    score = 0
    sentiment = "NEUTRAL"
    
    for word in NEGATIVE_KEYWORDS:
        if word in text_lower:
            score -= 1
    
    for word in POSITIVE_KEYWORDS:
        if word in text_lower:
            score += 1
            
    if score > 0:
        sentiment = "POSITIVE"
    elif score < 0:
        sentiment = "NEGATIVE"
        
    return {"score": score, "sentiment": sentiment, "text": text}

def get_stock_news(ticker: str) -> dict:
    """
    Mock function to simulate specific news fetching for a ticker.
    In a real app, you would search the news feed or use an API like NewsAPI.
    Here we simulate randomness or basic scraping results for demonstration.
    """
    # This is a placeholder since free real-time specific stock news APIs are rare without keys.
    # We will return a neutral structure or randomize for demo purposes.
    
    # In production: Filtering the global RSS feed for the ticker name
    return {
        "headline": "No specific major news found recently.",
        "sentiment": "NEUTRAL",
        "earnings_upcoming": False
    }

def fetch_global_market_mood():
    # Placeholder for Mocking "Morning Guard" logic
    # Real implementation would scrape moneycontrol/investing.com global indices
    return "NEUTRAL"
