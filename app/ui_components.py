import streamlit as st

def render_card(stock):
    st.markdown(f"""
    <div style="padding:10px; border-left: 5px solid {stock['ui_color'].lower()}; background-color: #222; border-radius: 5px; margin-bottom: 10px;">
        <h3>{stock['ticker']}</h3>
        <p>Price: {stock['technical']['price']} | EMA: {stock['technical']['ema']}</p>
        <p><b>RSI: {stock['technical']['rsi']}</b></p>
        <small>{stock.get('news', {}).get('headline', '')}</small>
        <div style="margin-top:5px; height:5px; width:100%; background:#444;">
            <div style="height:100%; width:{stock['confidence_score']}%; background:cyan;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
