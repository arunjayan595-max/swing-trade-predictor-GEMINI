import json
import os
from datetime import datetime

def save_daily_data(data, folder_path, filename_prefix="recommendations"):
    """
    Saves data to JSON with Deduplication logic.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{filename_prefix}_{date_str}.json"
    filepath = os.path.join(folder_path, filename)

    # DEDUPLICATION & MERGE LOGIC
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            existing_data = json.load(f)
        
        # Create a dict of existing stocks for O(1) lookup
        existing_stocks = {s['ticker']: s for s in existing_data.get('stocks', [])}
        
        # Merge new data (Overwrite duplicates with latest scan)
        for new_stock in data['stocks']:
            existing_stocks[new_stock['ticker']] = new_stock
            
        final_stocks = list(existing_stocks.values())
        data['stocks'] = final_stocks

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Data saved to {filepath}")
