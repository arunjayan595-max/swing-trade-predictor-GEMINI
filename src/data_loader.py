import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="1y"):
    """
    Fetches OHLCV data. Returns None if data is corrupt.
    """
    try:
        # Added .NS for NSE stocks if not present
        if not ticker.endswith(".NS"):
            ticker = f"{ticker}.NS"
            
        df = yf.download(ticker, period=period, progress=False)
        if df.empty:
            return None
        return df
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None
