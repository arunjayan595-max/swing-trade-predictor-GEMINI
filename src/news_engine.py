import random
from textblob import TextBlob
import json
import os
from datetime import datetime
import pandas as pd

def analyze_sentiment(ticker):
    # Simulation for V1 (Replace with Google News API later)
    headlines = [
        f"{ticker} reports growth.", f"Investors worried about {ticker}.", 
        f"{ticker} hits new high.", "Sector looks weak."
    ]
    headline = random.choice(headlines)
    blob = TextBlob(headline)
    score = blob.sentiment.polarity
    
    label = "NEUTRAL"
    if score > 0.1: label = "POSITIVE"
    if score < -0.1: label = "NEGATIVE"
    
    return {"headline": headline, "score": score, "label": label}

def run_news_scan():
    # Standalone Runner
    print("🗞️ Running News Scan...")
    tickers = pd.read_csv("config/tickers_nifty50.csv")['Ticker'].tolist()
    cache = {}
    for t in tickers:
        cache[t] = analyze_sentiment(t)
    
    os.makedirs("data/news", exist_ok=True)
    with open("data/news/sentiment_cache.json", "w") as f:
        json.dump(cache, f, indent=4)
    print("✅ News Cache Updated")

if __name__ == "__main__":
    run_news_scan()
