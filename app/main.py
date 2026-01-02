import streamlit as st
import json
import os
from app.ui_components import load_css  # <--- NEW IMPORT
from app.dashboard_pages import render_daily_view, render_weekly_view # <--- NEW IMPORT

st.set_page_config(page_title="Nifty Swing Predictor", layout="wide")

# Load CSS Styles
load_css()

# --- Helper Function ---
def load_latest_scan():
    folder = "data/daily"
    if not os.path.exists(folder): return None
    files = sorted(os.listdir(folder), reverse=True)
    if not files: return None
    with open(f"{folder}/{files[0]}", 'r') as f: return json.load(f)

# --- SIDEBAR ---
with st.sidebar:
    st.title("Navigation")
    view_mode = st.radio("Select View", ["Daily Action", "Weekly Structure"])
    
    st.divider()
    st.header("🧠 Emotional Log")
    with st.form("trade_journal"):
        st.text_input("Ticker")
        st.slider("FOMO Level", 1, 10)
        st.form_submit_button("Log Trade")

# --- MAIN AREA ---
st.title("📈 Swing Trade Nifty Predictor")
data = load_latest_scan()

if not data:
    st.error("No data found. Please run the scanner.")
else:
    st.caption(f"Last Scan: {data['meta']['date']} | Time: {data['meta']['scan_time']}")
    
    if view_mode == "Daily Action":
        render_daily_view(data)
    else:
        render_weekly_view(data)
