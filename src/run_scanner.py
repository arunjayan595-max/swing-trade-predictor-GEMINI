import pandas as pd
import yaml
from datetime import datetime
from data_loader import fetch_stock_data
from strategies import analyze_stock
from utils import save_daily_data

# Load Config
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

def run_analysis():
    print("Starting Post-Market Scan...")
    
    # Load Tickers
    tickers_df = pd.read_csv("config/tickers_nifty50.csv")
    ticker_list = tickers_df['Ticker'].tolist()
    
    results = []
    
    for ticker in ticker_list:
        print(f"Scanning {ticker}...")
        df = fetch_stock_data(ticker)
        
        if df is not None:
            analysis = analyze_stock(df, ticker, config)
            # Only save interesting stocks to keep JSON light
            if analysis['status'] != "BEARISH": 
                results.append(analysis)

    output_data = {
        "meta": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "market_mood": "NEUTRAL", # Placeholder for workflow 2 input
            "scan_time": datetime.now().strftime("%H:%M:%S")
        },
        "stocks": results
    }

    save_daily_data(output_data, config['paths']['daily_data'])

if __name__ == "__main__":
    run_analysis()
