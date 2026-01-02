import pandas as pd

def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def analyze_stock(df, ticker, config):
    """
    Applies the "Rule of 3":
    1. Price > 50 EMA
    2. RSI between 45 and 55 (Cooling period/Pullback)
    """
    # 1. Calculate Indicators
    df['EMA_50'] = df['Close'].ewm(span=config['indicators']['ema_period'], adjust=False).mean()
    df['RSI'] = calculate_rsi(df['Close'], config['indicators']['rsi_period'])

    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    price = last_row['Close']
    ema_50 = last_row['EMA_50']
    rsi = last_row['RSI']

    # 2. The Strategy Logic
    status = "WAIT"
    ui_color = "GRAY"
    confidence = 0

    # Rule: Price is above EMA 50 AND RSI is in "Sweet Spot"
    if price > ema_50:
        if config['indicators']['rsi_min'] <= rsi <= config['indicators']['rsi_max']:
            status = "BUY WATCH"
            ui_color = "GREEN"
            confidence = 80
        elif rsi > 70:
            status = "OVERBOUGHT"
            ui_color = "RED"
        else:
            status = "HOLD"
            ui_color = "YELLOW"
            confidence = 50
    else:
        status = "BEARISH"
        ui_color = "RED"

    return {
        "ticker": ticker,
        "status": status,
        "ui_color": ui_color,
        "technical": {
            "price": round(float(price), 2),
            "ema_50": round(float(ema_50), 2),
            "rsi": round(float(rsi), 2)
        },
        "confidence_score": confidence
    }
