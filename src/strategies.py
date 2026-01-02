import pandas as pd

def apply_strategy(df, ticker, config):
    # 1. Calculate Indicators
    df['EMA'] = df['Close'].ewm(span=config['indicators']['ema_period'], adjust=False).mean()
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    current = df.iloc[-1]
    
    # 2. Strategy Logic
    price = current['Close']
    ema = current['EMA']
    rsi = current['RSI']
    
    status = "WAIT"
    color = "GRAY"
    score = 0
    
    # RULE OF 3: Price > EMA + RSI in Sweet Spot (45-55)
    if price > ema:
        if 45 <= rsi <= 55:
            status = "BUY WATCH"
            color = "GREEN"
            score = 80
        elif rsi > 70:
            status = "OVERBOUGHT"
            color = "RED"
        else:
            status = "HOLD"
            color = "YELLOW"
            score = 50
    else:
        status = "BEARISH"
        color = "RED"
        
    return {
        "ticker": ticker,
        "status": status,
        "ui_color": color,
        "technical": {
            "price": round(float(price), 2),
            "ema": round(float(ema), 2),
            "rsi": round(float(rsi), 2)
        },
        "confidence_score": score
    }
