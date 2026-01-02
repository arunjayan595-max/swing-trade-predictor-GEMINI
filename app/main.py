import streamlit as st
import json
import os
import glob
from ui_components import render_card

st.set_page_config(layout="wide", page_title="Swing Predictor")

# Helper to load latest file
def get_latest_data(folder):
    files = glob.glob(f"{folder}/*.json")
    if not files: return None
    latest_file = max(files, key=os.path.getctime)
    with open(latest_file) as f: return json.load(f)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Daily Scanner", "Weekly Structure"])

if page == "Daily Scanner":
    st.title("🚀 Daily Swing Signals")
    data = get_latest_data("data/daily")
    
    if data:
        st.info(f"Market Mood: {data['meta']['market_mood']} | Date: {data['meta']['date']}")
        
        # Actionable Green Stocks
        st.subheader("✅ Buy Watchlist")
        cols = st.columns(3)
        greens = [s for s in data['stocks'] if s['ui_color'] == 'GREEN']
        
        if not greens: st.write("No signals today.")
        
        for idx, stock in enumerate(greens):
            with cols[idx % 3]:
                render_card(stock)
                
        # Watchlist Yellow Stocks
        st.subheader("⚠️ Setup Forming")
        yellows = [s for s in data['stocks'] if s['ui_color'] == 'YELLOW']
        for stock in yellows:
            st.text(f"{stock['ticker']} - RSI: {stock['technical']['rsi']}")
            
    else:
        st.error("No Data Found. GitHub Actions haven't run yet.")

elif page == "Weekly Structure":
    st.title("📅 Weekly Trends")
    data = get_latest_data("data/weekly")
    if data:
        st.table(data['stocks'])
    else:
        st.error("No Weekly Data Found.")
