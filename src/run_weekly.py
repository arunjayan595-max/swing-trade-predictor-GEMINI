import pandas as pd
import yaml
from src.data_loader import fetch_data
from src.utils import save_json_data

def main():
    print("📅 Running Weekly Scan...")
    with open("config/settings.yaml") as f: config = yaml.safe_load(f)
    tickers = pd.read_csv("config/tickers_nifty50.csv")['Ticker'].tolist()
    
    results = []
    for ticker in tickers:
        df = fetch_data(ticker, period="2y", interval="1wk")
        if df is not None:
            df['EMA50'] = df['Close'].ewm(span=50).mean()
            price = df['Close'].iloc[-1]
            ema = df['EMA50'].iloc[-1]
            
            # Simple Weekly Check
            status = "BULLISH TREND" if price > ema else "BEARISH TREND"
            dist = ((price - ema) / price) * 100
            
            if abs(dist) < 3: status = "AT KEY SUPPORT/RESISTANCE"
            
            results.append({
                "ticker": ticker, "weekly_status": status, 
                "price": round(float(price), 2), "weekly_ema": round(float(ema), 2)
            })
            
    save_json_data({"stocks": results}, config['paths']['weekly'], "weekly_scan")

if __name__ == "__main__":
    main()
