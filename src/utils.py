import os
import json
import logging
from datetime import datetime

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_directory(path: str):
    """Ensure that a directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Created directory: {path}")

def save_json(data: dict, filepath: str):
    """Save dictionary to JSON file."""
    ensure_directory(os.path.dirname(filepath))
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved data to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save JSON to {filepath}: {e}")

def load_json(filepath: str) -> dict:
    """Load dictionary from JSON file."""
    if not os.path.exists(filepath):
        logger.warning(f"File not found: {filepath}")
        return {}
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON from {filepath}: {e}")
        return {}

def get_today_date_str() -> str:
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime('%Y-%m-%d')
