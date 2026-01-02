import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .stock-card {
            background-color: #1E1E1E;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #555;
            margin-bottom: 10px;
        }
        .card-green { border-left-color: #00FF00; }
        .card-yellow { border-left-color: #FFD700; }
        .card-red { border-left-color: #FF0000; }
        
        .metric-label { font-size: 0.8em; color: #888; }
        .metric-value { font-size: 1.2em; font-weight: bold; color: #FFF; }
        
        .news-badge {
            background-color: #333;
            color: #DDD;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7em;
        }
    </style>
    """, unsafe_allow_html=True)

def render_stock_card(stock):
    """
    Renders a custom HTML card for a stock.
    """
    color_class = f"card-{stock['ui_color'].lower()}"
    
    # Simple HTML structure for the card
    html = f"""
    <div class="stock-card {color_class}">
        <div style="display:flex; justify-content:space-between;">
            <h3 style="margin:0;">{stock['ticker']}</h3>
            <span style="color:{stock['ui_color']}">{stock['status']}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:10px;">
            <div>
                <div class="metric-label">Price</div>
                <div class="metric-value">₹{stock['technical']['price']}</div>
            </div>
            <div>
                <div class="metric-label">RSI</div>
                <div class="metric-value">{stock['technical']['rsi']}</div>
            </div>
            <div>
                <div class="metric-label">Confidence</div>
                <div class="metric-value">{stock['confidence_score']}%</div>
            </div>
        </div>
        <div style="margin-top:8px; font-size:0.8em; color:#AAA;">
            📰 {stock.get('news_analysis', {}).get('top_headline', 'No News')}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
