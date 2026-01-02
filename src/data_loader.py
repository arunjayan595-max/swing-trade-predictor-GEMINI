import yfinance as yf

def fetch_data(ticker, period="1y", interval="1d"):
    if not ticker.endswith(".NS"):
        ticker = f"{ticker}.NS"
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        return df if not df.empty else None
    except:
        return None
