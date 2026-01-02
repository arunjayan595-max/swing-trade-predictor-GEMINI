import json
import os
from datetime import datetime

def save_json_data(new_data, folder, filename_prefix):
    """
    Robust saver: Creates folders, merges duplicates, saves JSON.
    """
    os.makedirs(folder, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(folder, f"{filename_prefix}_{date_str}.json")

    final_data = new_data

    # Merge logic: If file exists, update specific stocks, don't overwrite everything
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                existing = json.load(f)
            
            # Create dict for fast lookup
            existing_stocks = {s['ticker']: s for s in existing.get('stocks', [])}
            
            # Update with new data
            for stock in new_data.get('stocks', []):
                existing_stocks[stock['ticker']] = stock
            
            final_data['stocks'] = list(existing_stocks.values())
            final_data['meta'] = new_data['meta'] # Update timestamp
        except Exception as e:
            print(f"Warning: Could not merge data, overwriting. Error: {e}")

    with open(filepath, 'w') as f:
        json.dump(final_data, f, indent=4)
    print(f"✅ Data saved to {filepath}")

def load_json_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}
