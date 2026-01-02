import streamlit as st
import os
import sys

# Ensure src is in pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ui_components import load_custom_css
from app.dashboard_pages import render_dashboard_page

st.set_page_config(
    page_title="Swing Trade Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
load_custom_css()

# Sidebar
st.sidebar.title("Nifty Predictor 🚀")
page = st.sidebar.radio("Navigate", ["Daily Signals", "Weekly Picks", "Strategy Sandbox"])

# Paths
DAILY_DATA_DIR = os.path.join(os.getcwd(), 'data', 'daily')
WEEKLY_DATA_DIR = os.path.join(os.getcwd(), 'data', 'weekly')

if page == "Daily Signals":
    render_dashboard_page("Daily Market Action", DAILY_DATA_DIR)

elif page == "Weekly Picks":
    render_dashboard_page("Weekly Smart Picks", WEEKLY_DATA_DIR)

elif page == "Strategy Sandbox":
    st.header("🧪 Strategy Sandbox")
    st.write("Coming soon: Backtest your strategies against historical data.")
    
    # Emotional Log (Placeholder from user request)
    st.subheader("Emotional Log")
    confidence = st.slider("How confident are you right now?", 1, 10, 5)
    fomo = st.checkbox("Are you feeling FOMO?")
    if st.button("Log Emotion"):
        st.success(f"Logged: Confidence {confidence}/10, FOMO: {fomo}")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("v1.0 | Data: Yahoo Finance")
