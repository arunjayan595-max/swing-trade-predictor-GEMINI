import streamlit as st
import pandas as pd
from app.ui_components import render_stock_card

def render_daily_view(data):
    st.subheader("🚀 Daily Sniper Scan")
    
    # Filter Controls
    col1, col2 = st.columns(2)
    with col1:
        min_conf = st.slider("Min Confidence Score", 0, 100, 60)
    with col2:
        show_only_buy = st.checkbox("Show BUY Only", value=True)

    # Logic to filter stocks
    stocks = data.get('stocks', [])
    filtered_stocks = [
        s for s in stocks 
        if s['confidence_score'] >= min_conf
        and (s['status'] == "BUY WATCH" if show_only_buy else True)
    ]

    if not filtered_stocks:
        st.info("No stocks match your filters.")
    else:
        for stock in filtered_stocks:
            render_stock_card(stock)

def render_weekly_view(data):
    st.subheader("📅 Weekly Structural View")
    st.write("This view shows stocks near major Weekly Support zones.")
    # In V1, we can reuse the daily logic or load a different JSON file
    # For now, we display a placeholder table
    if 'stocks' in data:
        df = pd.DataFrame(data['stocks'])
        st.dataframe(df[['ticker', 'technical']])
