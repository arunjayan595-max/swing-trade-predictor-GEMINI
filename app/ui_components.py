import streamlit as st

def load_custom_css():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stock-card {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            border: 1px solid #333;
        }
        .card-green {
            background-color: #1b4b35; /* Dark Green */
            border-left: 5px solid #00c853;
        }
        .card-yellow {
            background-color: #4b4b1b; /* Dark Yellow */
            border-left: 5px solid #ffd600;
        }
        .card-red {
            background-color: #4b1b1b; /* Dark Red */
            border-left: 5px solid #d50000;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
        }
        .metric-label {
            font-size: 0.8rem;
            color: #aaa;
        }
        .confidence-meter {
            height: 10px;
            background-color: #333;
            border-radius: 5px;
            margin-top: 10px;
        }
        .meter-fill {
            height: 100%;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

def render_stock_card(stock: dict):
    color_class = f"card-{stock['ui_color'].lower()}" if stock['ui_color'] in ['GREEN', 'YELLOW', 'RED'] else "card-yellow"
    
    st.markdown(f"""
        <div class="stock-card {color_class}">
            <h3>{stock['ticker']} <span style="font-size: 0.8em; float: right;">{stock['status']}</span></h3>
            <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                <div>
                    <div class="metric-label">Price</div>
                    <div class="metric-value">₹{stock['technical']['price']}</div>
                </div>
                <div>
                    <div class="metric-label">EMA 50</div>
                    <div class="metric-value">₹{stock['technical']['ema_50']}</div>
                </div>
                <div>
                    <div class="metric-label">RSI</div>
                    <div class="metric-value">{stock['technical']['rsi']}</div>
                </div>
            </div>
            <div style="margin-top: 15px;">
                <div class="metric-label">News Sentiment</div>
                <div>{stock['news_analysis']['sentiment']}</div>
            </div>
             <div class="confidence-meter">
                <div class="meter-fill" style="width: {stock['confidence_score']}%; background-color: {getColor(stock['confidence_score'])};"></div>
            </div>
            <div style="text-align: right; font-size: 0.7em; margin-top: 5px;">Confidence: {stock['confidence_score']}%</div>
        </div>
    """, unsafe_allow_html=True)

def getColor(score):
    if score >= 70: return "#00c853"
    if score >= 40: return "#ffd600"
    return "#d50000"
