import yfinance as yf
import json
import os
from datetime import datetime

def check_mood():
    print("🌍 Checking Global Cues...")
    # S&P500 and Nifty
    data = yf.download(["^GSPC", "^NSEI"], period="2d", progress=False)['Close']
    
    try:
        # Calculate US Market change
        us_change = ((data['^GSPC'].iloc[-1] - data['^GSPC'].iloc[-2]) / data['^GSPC'].iloc[-2]) * 100
        
        mood = "NEUTRAL"
        if us_change > 0.75: mood = "BULLISH (Gap Up Likely)"
        if us_change < -0.75: mood = "BEARISH (Gap Down Likely)"
        
        output = {"date": datetime.now().strftime("%Y-%m-%d"), "mood": mood, "us_change": us_change}
        
        os.makedirs("data/daily", exist_ok=True)
        with open("data/daily/market_mood.json", "w") as f:
            json.dump(output, f, indent=4)
        print(f"✅ Mood set to: {mood}")
        
    except Exception as e:
        print(f"❌ Error checking mood: {e}")

if __name__ == "__main__":
    check_mood()
