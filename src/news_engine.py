import requests
from textblob import TextBlob # Requires: pip install textblob
import random

# Mocking a news fetch for stability in V1 (Real APIs usually require keys)
# In V2, you would replace 'generate_mock_news' with 'fetch_google_news'
def get_stock_news(ticker):
    """
    Fetches news and calculates a sentiment score (-1 to 1).
    """
    # 1. Define Search Keywords associated with the stock
    stock_name = ticker.replace(".NS", "")
    
    # 2. Simulation of fetching headlines (Replace with RSS FeedParser later)
    # logic: In a real app, use 'GoogleNews' library here.
    headlines = [
        f"{stock_name} announces strong quarterly results",
        f"Market cautious ahead of {stock_name} AGM",
        f"Analyst upgrades {stock_name} to Buy",
        f"Sector headwinds might affect {stock_name}"
    ]
    
    # 3. Analyze Sentiment using TextBlob (NLP)
    total_polarity = 0
    relevant_headlines = []
    
    for headline in headlines:
        # Simple randomization to simulate changing news for V1 demo
        if random.random() > 0.5: 
            analysis = TextBlob(headline)
            score = analysis.sentiment.polarity
            total_polarity += score
            relevant_headlines.append({
                "headline": headline,
                "sentiment": round(score, 2)
            })

    # Average sentiment
    avg_score = total_polarity / len(relevant_headlines) if relevant_headlines else 0
    
    # Determine Label
    if avg_score > 0.1: sentiment_label = "POSITIVE"
    elif avg_score < -0.1: sentiment_label = "NEGATIVE"
    else: sentiment_label = "NEUTRAL"

    return {
        "sentiment_score": round(avg_score, 2),
        "sentiment_label": sentiment_label,
        "top_headline": relevant_headlines[0]['headline'] if relevant_headlines else "No recent news"
    }
