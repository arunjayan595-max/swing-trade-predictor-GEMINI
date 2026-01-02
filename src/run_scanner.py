import pandas as pd
import yaml
from datetime import datetime
# Note: Using absolute imports assuming script is run via 'python -m src.run_scanner'
from src.data_loader import fetch_data
from src.strategies import apply_strategy
from src.news_engine import analyze_sentiment
from src.utils import save_json_data, load_json_file

def main():
    print("🚀 Starting Main Scanner...")
    
    # 1. Load Config
    with open("config/settings.yaml") as f: config = yaml.safe_load(f)
    tickers = pd.read_csv("config/tickers_nifty50.csv")['Ticker'].tolist()
    
    # 2. Load Market Mood (Prevent crash if missing)
    mood_data = load_json_file(config['paths']['mood'])
    market_mood = mood_data.get('mood', 'NEUTRAL')
    
    results = []
    
    for ticker in tickers:
        print(f"Scanning {ticker}...")
        df = fetch_data(ticker)
        
        if df is not None:
            # A. Run Strategy
            analysis = apply_strategy(df, ticker, config)
            
            # B. Integrate News (if stock is interesting)
            if analysis['ui_color'] != "RED":
                news = analyze_sentiment(ticker)
                analysis['news'] = news
                
                # Adjust Score based on News & Market Mood
                if news['label'] == "POSITIVE": analysis['confidence_score'] += 10
                if news['label'] == "NEGATIVE": analysis['confidence_score'] -= 10
                if market_mood == "BEARISH (Gap Down Likely)": analysis['confidence_score'] -= 15
                
                # Cap Score
                analysis['confidence_score'] = max(0, min(100, analysis['confidence_score']))
                
                results.append(analysis)
    
    # 3. Save Output
    output = {
        "meta": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "market_mood": market_mood,
            "scan_time": datetime.now().strftime("%H:%M:%S")
        },
        "stocks": results
    }
    
    save_json_data(output, config['paths']['daily'], "recommendations")

if __name__ == "__main__":
    main()
