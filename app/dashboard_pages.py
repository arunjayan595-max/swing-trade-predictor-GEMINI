import streamlit as st
import os
import json
from .ui_components import render_stock_card

def render_dashboard_page(section_title: str, folder_path: str):
    st.header(section_title)
    
    # List available JSON files
    try:
        files = sorted([f for f in os.listdir(folder_path) if f.endswith('.json')], reverse=True)
    except FileNotFoundError:
        st.warning(f"No data directory found at {folder_path}")
        return

    if not files:
        st.info("No scan results available yet.")
        return

    selected_file = st.selectbox(f"Select Report ({section_title})", files)
    
    if selected_file:
        file_path = os.path.join(folder_path, selected_file)
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        st.caption(f"Date: {data.get('meta', {}).get('date', 'Unknown')}")
        
        stocks = data.get('stocks', [])
        if not stocks:
            st.warning("No stocks found in this report.")
        
        # Grid layout for cards
        cols = st.columns(3)
        for i, stock in enumerate(stocks):
            with cols[i % 3]:
                render_stock_card(stock)
