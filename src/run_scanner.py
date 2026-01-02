import argparse
import sys
import os
import pandas as pd
import logging

# Ensure src in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.screener_tools import run_weekly_scan, run_daily_scan
from src.utils import ensure_directory

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_tickers():
    path = os.path.join(os.getcwd(), 'config', 'tickers_nifty50.csv')
    try:
        df = pd.read_csv(path)
        return df['Ticker'].tolist()
    except Exception as e:
        logger.error(f"Failed to load tickers: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Swing Trade Predictor Scanner")
    parser.add_argument('--mode', type=str, required=True, 
                        choices=['weekly', 'daily', 'pre_market', 'news'],
                        help="Scan mode to execute")
    
    args = parser.parse_args()
    
    tickers = load_tickers()
    if not tickers:
        logger.error("No tickers found. Exiting.")
        sys.exit(1)
        
    if args.mode == 'weekly':
        logger.info("Starting Weekly Scan...")
        run_weekly_scan(tickers)
        
    elif args.mode == 'daily':
        logger.info("Starting Daily Scan...")
        run_daily_scan(tickers)
        
    elif args.mode == 'pre_market':
        logger.info("Pre-Market checks not yet implemented.")
        
    elif args.mode == 'news':
        logger.info("News fetching not yet implemented.")

if __name__ == "__main__":
    main()
