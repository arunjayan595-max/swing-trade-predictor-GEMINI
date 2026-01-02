import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(page_title="Nifty Swing Predictor", layout="wide")

# --- Helper Functions ---
def load_latest_scan():
    folder = "data/daily"
    if not os.path.exists(folder):
        return None
    files = sorted(os.listdir(folder), reverse=True)
    if not files:
        return None
    
    with open(f"{folder}/{files[0]}", 'r') as f:
        return json.load(f)

# --- SIDEBAR: Backtesting & Psychology Module ---
with st.sidebar:
    st.header("🧠 Emotional Log & Backtest")
    st.info("Track your psychology before taking the trade.")
    
    with st.form("trade_journal"):
        selected_ticker = st.text_input("Ticker Symbol")
        fomo_score = st.slider("FOMO Level (1-10)", 1, 10, 1)
        confidence = st.slider("Confidence Level", 1, 100, 50)
        notes = st.text_area("Why are you taking this trade?")
        
        submitted = st.form_submit_button("Log Trade Simulation")
        if submitted:
            # Logic to save to 'data/history' would go here
            st.success(f"Logged {selected_ticker}. Don't let FOMO rule you!")

# --- MAIN DASHBOARD ---
st.title("📈 Swing Trade Nifty Predictor")

data = load_latest_scan()

if not data:
    st.warning("No scan data found. Please run the GitHub Action.")
else:
    meta = data['meta']
    st.markdown(f"**Date:** {meta['date']} | **Market Mood:** {meta['market_mood']}")
    
    # Filter for Green/Actionable Stocks
    stocks = data['stocks']
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Top Picks (Rule of 3)")
        
        for stock in stocks:
            if stock['ui_color'] == 'GREEN':
                with st.expander(f"✅ {stock['ticker']} - Score: {stock['confidence_score']}", expanded=True):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Price", f"₹{stock['technical']['price']}")
                    c2.metric("50 EMA", f"₹{stock['technical']['ema_50']}")
                    c3.metric("RSI", stock['technical']['rsi'])
                    
                    st.caption(f"Status: {stock['status']}")
                    
                    # Risk Reward Calculator (Efficiency Feature B)
                    sl = stock['technical']['ema_50'] * 0.98 # Example dynamic SL
                    target = stock['technical']['price'] * 1.05
                    risk = stock['technical']['price'] - sl
                    reward = target - stock['technical']['price']
                    rr_ratio = round(reward/risk, 2)
                    
                    st.markdown(f"**R:R Ratio:** 1:{rr_ratio}")
                    if rr_ratio < 2:
                        st.error("⚠️ Risk/Reward < 1:2. Trade not recommended.")
                    else:
                        st.success("🚀 Good Risk/Reward setup.")

    with col2:
        st.subheader("⚠️ Watchlist (Setup Forming)")
        df_watch = pd.DataFrame([s for s in stocks if s['ui_color'] == 'YELLOW'])
        if not df_watch.empty:
            st.dataframe(df_watch[['ticker', 'status']])
        else:
            st.write("No setups forming.")
