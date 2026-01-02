import pandas as pd
import yaml
from datetime import datetime
from src.data_loader import fetch_stock_data
from src.strategies import analyze_stock
from src.news_engine import get_stock_news  # <--- NEW IMPORT
from src.utils import save_daily_data

# Load Config
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

def run_analysis():
    print("Starting Post-Market Scan...")
    
    tickers_df = pd.read_csv("config/tickers_nifty50.csv")
    ticker_list = tickers_df['Ticker'].tolist()
    
    results = []
    
    for ticker in ticker_list:
        print(f"Scanning {ticker}...")
        df = fetch_stock_data(ticker)
        
        if df is not None:
            # 1. Technical Analysis
            analysis = analyze_stock(df, ticker, config)
            
            # 2. News Analysis (Only if technicals are interesting)
            # This saves API calls/time by not scanning bearish stocks
            if analysis['status'] != "BEARISH":
                print(f"   -> Fetching news for {ticker}")
                news_data = get_stock_news(ticker)
                
                # Merge News into Analysis
                analysis['news_analysis'] = news_data
                
                # Adjust Confidence based on News
                if news_data['sentiment_label'] == "POSITIVE":
                    analysis['confidence_score'] += 10
                elif news_data['sentiment_label'] == "NEGATIVE":
                    analysis['confidence_score'] -= 20
                
                # Cap confidence at 100
                analysis['confidence_score'] = min(100, analysis['confidence_score'])
                
                results.append(analysis)

    output_data = {
        "meta": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "scan_time": datetime.now().strftime("%H:%M:%S")
        },
        "stocks": results
    }

    save_daily_data(output_data, config['paths']['daily_data'])

if __name__ == "__main__":
    run_analysis()
