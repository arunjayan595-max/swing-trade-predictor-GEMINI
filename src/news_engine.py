# ... existing code ...

def refresh_news_cache():
    """
    Standalone function to scan all tickers and save a news dump.
    """
    import pandas as pd
    import json
    import os
    from datetime import datetime

    print("Refreshing News Cache...")
    tickers_df = pd.read_csv("config/tickers_nifty50.csv")
    tickers = tickers_df['Ticker'].tolist()
    
    news_cache = {}
    
    for ticker in tickers:
        print(f"Fetching news for {ticker}...")
        news_data = get_stock_news(ticker) # Uses the function defined earlier
        news_cache[ticker] = news_data
        
    # Save to data/news/sentiment_cache.json
    os.makedirs("data/news", exist_ok=True)
    with open("data/news/sentiment_cache.json", "w") as f:
        json.dump({
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": news_cache
        }, f, indent=4)

if __name__ == "__main__":
    refresh_news_cache()
