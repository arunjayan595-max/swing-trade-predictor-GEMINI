import pandas as pd
import yaml
import os
from data_loader import fetch_stock_data
from utils import save_daily_data
from datetime import datetime

# Load Config
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

def run_weekly_scan():
    print("Starting Weekly Structural Scan...")
    tickers_df = pd.read_csv("config/tickers_nifty50.csv")
    ticker_list = tickers_df['Ticker'].tolist()
    
    weekly_results = []
    
    for ticker in ticker_list:
        # Fetch Daily data but we will resample it to Weekly
        df = fetch_stock_data(ticker, period="2y") # Need more data for weekly EMA
        
        if df is not None:
            # Resample to Weekly
            # Logic: Take the last price of the week, max high, min low
            weekly_df = df.resample('W').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            })
            
            # Calculate Weekly EMA (Long term trend)
            weekly_df['EMA_50'] = weekly_df['Close'].ewm(span=50, adjust=False).mean()
            
            last_wk = weekly_df.iloc[-1]
            
            # Weekly Strategy: Is it near the 50 Weekly EMA? (Major Support)
            price = last_wk['Close']
            ema = last_wk['EMA_50']
            
            # If price is within 3% of Weekly EMA, it's a "Major Support Zone"
            diff_pct = abs(price - ema) / price
            
            status = "NEUTRAL"
            if price > ema and diff_pct < 0.03:
                status = "AT WEEKLY SUPPORT"
            elif price < ema:
                status = "WEEKLY BEARISH"
            else:
                status = "WEEKLY BULLISH"

            weekly_results.append({
                "ticker": ticker,
                "weekly_status": status,
                "price": round(price, 2),
                "weekly_ema": round(ema, 2)
            })

    # Save to data/weekly/
    output = {
        "meta": {"date": datetime.now().strftime("%Y-%m-%d"), "type": "WEEKLY"},
        "stocks": weekly_results
    }
    
    # Custom save location
    folder = "data/weekly"
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/weekly_scan_{datetime.now().strftime('%Y-%m-%d')}.json", "w") as f:
        import json
        json.dump(output, f, indent=4)

if __name__ == "__main__":
    run_weekly_scan()
