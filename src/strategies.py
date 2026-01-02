import pandas as pd
import pandas_ta as ta
import yaml
import os

# Load Settings
CONFIG_PATH = os.path.join(os.getcwd(), 'config', 'settings.yaml')

def load_settings():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    except:
        return {} # Fallback

settings = load_settings()
EMA_PERIOD = settings.get('indicators', {}).get('ema', {}).get('period', 50)
RSI_PERIOD = settings.get('indicators', {}).get('rsi', {}).get('period', 14)
RSI_MIN = settings.get('indicators', {}).get('rsi', {}).get('buy_range_min', 45)
RSI_MAX = settings.get('indicators', {}).get('rsi', {}).get('buy_range_max', 55)

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate EMA and RSI."""
    if df.empty:
        return df
    
    # Ensure numeric columns
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    
    # EMA
    df[f'EMA_{EMA_PERIOD}'] = ta.ema(df['Close'], length=EMA_PERIOD)
    
    # RSI
    df['RSI'] = ta.rsi(df['Close'], length=RSI_PERIOD)
    
    return df

def analyze_stock(df: pd.DataFrame) -> dict:
    """
    Analyze the latest state of the stock based on "Rule of 3".
    
    Returns:
        Dictionary with status, technical values, and confidence.
    """
    if df.empty or len(df) < EMA_PERIOD:
        return {"status": "NEUTRAL", "reason": "Insufficient Data"}

    last_row = df.iloc[-1]
    price = last_row['Close']
    ema = last_row.get(f'EMA_{EMA_PERIOD}', 0)
    rsi = last_row.get('RSI', 50)
    
    result = {
        "price": round(price, 2),
        "ema_50": round(ema, 2),
        "rsi": round(rsi, 2),
        "status": "HOLD",
        "ui_color": "YELLOW",
        "confidence_score": 50,
        "reason": "Waiting for signal"
    }

    # Strategy Logic
    # 1. Price > EMA 50
    above_ema = price > ema
    
    # 2. RSI in Buying Range (45-55) or cooling off (e.g., < 60 but bullish)
    # User specified "RSI 45-55" as a key criteria for entry
    rsi_setup = RSI_MIN <= rsi <= RSI_MAX
    
    if above_ema and rsi_setup:
        result["status"] = "BUY"
        result["ui_color"] = "GREEN"
        result["confidence_score"] = 80
        result["reason"] = "Price > 50EMA & RSI in Golden Zone"
    elif not above_ema:
        result["status"] = "SELL/AVOID"
        result["ui_color"] = "RED"
        result["confidence_score"] = 20
        result["reason"] = "Price below 50EMA"
    
    return result

def calculate_risk_reward(entry, stop_loss):
    risk = entry - stop_loss
    if risk <= 0: return 0
    # Assuming standard 2:1 target for simple calc
    target = entry + (risk * 2)
    return target
