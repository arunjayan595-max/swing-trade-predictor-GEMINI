# Swing Trade Nifty Predictor

A modular, future-proof Swing Trade Predictor for Nifty stocks. The system separates Backend (Data Collection via Github Actions) from Frontend (Streamlit Visualization), using the repository as the database.

## Architecture
- **Backend**: Github Actions (Fetch prices, screen stocks)
- **Database**: JSON/CSV files in `data/` directory
- **Frontend**: Streamlit Dashboard

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   streamlit run app/main.py
   ```
