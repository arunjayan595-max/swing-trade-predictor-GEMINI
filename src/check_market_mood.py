import yfinance as yf
import json
import os
from datetime import datetime

def analyze_market_mood():
    # Tickers for Global Cues
    # ^GSPC = S&P 500 (US)
    # ^NSEI = Nifty 50 (India - Previous Close)
    tickers = ["^GSPC", "^NSEI"] 
    
    print("Fetching Global Cues...")
    data = yf.download(tickers, period="2d", progress=False)['Close']
    
    mood = "NEUTRAL"
    details = {}

    try:
        # Check US Markets (Yesterday's Close)
        sp500_today = data['^GSPC'].iloc[-1]
        sp500_prev = data['^GSPC'].iloc[-2]
        sp500_change = ((sp500_today - sp500_prev) / sp500_prev) * 100
        
        details['US_Market_Change'] = round(sp500_change, 2)

        # Logic: If US Market moved > 1%, likely Gap Up/Down
        if sp500_change > 0.8:
            mood = "BULLISH (Gap Up Likely)"
        elif sp500_change < -0.8:
            mood = "BEARISH (Gap Down Likely)"
        else:
            mood = "NEUTRAL"

    except Exception as e:
        print(f"Error calculating mood: {e}")
        mood = "UNKNOWN"

    # Save to JSON
    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "mood": mood,
        "global_cues": details
    }
    
    # Ensure directory exists
    os.makedirs("data/daily", exist_ok=True)
    
    with open("data/daily/market_mood.json", "w") as f:
        json.dump(output, f, indent=4)
    
    print(f"Market Mood Updated: {mood}")

if __name__ == "__main__":
    analyze_market_mood()
