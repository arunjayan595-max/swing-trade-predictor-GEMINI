import yfinance as yf
import pandas as pd
import os
import logging
from .utils import ensure_directory

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.getcwd(), 'data', 'history')

def fetch_stock_data(ticker: str, period: str = "2y") -> pd.DataFrame:
    """
    Fetch stock data from yfinance.
    
    Args:
        ticker: Stock ticker symbol (e.g., "RELIANCE.NS")
        period: Data period to fetch
        
    Returns:
        DataFrame with OHLCV data
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        if df.empty:
            logger.warning(f"No data found for {ticker}")
            return pd.DataFrame()
        
        # Ensure proper Index and Column formatting
        df.reset_index(inplace=True)
        # Convert Date to datetime if not already
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def save_and_update_data(ticker: str, new_df: pd.DataFrame):
    """
    Save stock data to CSV, merging with existing data to ensure deduplication.
    
    Args:
        ticker: Stock ticker symbol
        new_df: New data to merge
    """
    if new_df.empty:
        return

    filepath = os.path.join(DATA_DIR, f"{ticker}.csv")
    ensure_directory(DATA_DIR)
    
    combined_df = new_df
    
    if os.path.exists(filepath):
        try:
            existing_df = pd.read_csv(filepath)
            existing_df['Date'] = pd.to_datetime(existing_df['Date']).dt.date
            
            # Combine and deduplicate
            # We use 'Date' as primary key for deduplication
            combined_df = pd.concat([existing_df, new_df])
            combined_df.drop_duplicates(subset=['Date'], keep='last', inplace=True)
            combined_df.sort_values(by='Date', inplace=True)
        except Exception as e:
            logger.error(f"Error reading existing file {filepath}: {e}")
            # If read fails, valid new_df becomes the file content (overwrite corrupted)
    
    try:
        combined_df.to_csv(filepath, index=False)
        logger.info(f"Updated data for {ticker} at {filepath}")
    except Exception as e:
        logger.error(f"Failed to save data for {ticker}: {e}")

def load_stock_data(ticker: str) -> pd.DataFrame:
    """Load local stock data."""
    filepath = os.path.join(DATA_DIR, f"{ticker}.csv")
    if not os.path.exists(filepath):
        return pd.DataFrame()
    return pd.read_csv(filepath)
