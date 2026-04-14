import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- KONFIGURASJON & STIL ---
BI_DARK_BLUE = "#00244E"
BI_LIGHT_BLUE = "#4C76BA"
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#00ADBA" # Turkis for kontrast

st.set_page_config(page_title="Finans Dashboard", layout="wide")

# Custom CSS for å tvinge BI-farger og logo-plassering
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BI_DARK_BLUE};
        color: {TEXT_COLOR};
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    h1, h2, h3, p {{
        color: {TEXT_COLOR} !important;
    }}
    /* Logo i øverste høyre hjørne */
    .logo-container {{
        position: absolute;
        top: -50px;
        right: 0px;
    }}
    </style>
    """, unsafe_allow_stdio=True)

# --- LOGO OG TITTEL ---
# Erstatt URL-en under med din egen logo-filvei eller URL
LOGO_URL = "https://www.bi.no/globalassets/images/logo/bi_logo_white.png" 

col1, col2 = st.columns([4, 1])
with col1:
    st.title("📊 Markedsanalyse: Norge & Krypto")
with col2:
    st.image(LOGO_URL, width=150)

# --- DATAHENTING ---
def get_data(ticker, period="1mo"):
    data = yf.download(ticker, period=period, interval="1d")
    return data

# Definer markeder (OSEBX for Norge, BTC + Ethereum & Solana)
assets = {
    "OSEBX (Oslo Børs)": "^OSEBX",
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD"
}

# --- VISUALISERING ---
st.markdown("---")
cols = st.columns(len(assets))

for i, (name, ticker) in enumerate(assets.items()):
    df = get_data(ticker)
    
    if not df.empty:
        current_price = df['Close'].iloc[-1].values[0]
        prev_price = df['Close'].iloc[-2].values[0]
        delta = ((current_price - prev_price) / prev_price) * 100

        with cols[i]:
            # Metric-visning
            st.metric(label=name, value=f"{current_price:,.2f}", delta=f"{delta:.2f}%")
            
            # Graf
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.index, 
                y=df['Close'].iloc[:, 0],
                mode='lines',
                line=dict(color=ACCENT_COLOR, width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 173, 186, 0.1)'
            ))
            
            fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=150,
                xaxis_visible=False,
                yaxis_visible=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- DETALJERT GRAF ---
st.markdown("### Markedsutvikling (Siste 30 dager)")
selected_asset = st.selectbox("Velg aktivum for detaljer", list(assets.keys()))
detail_df = get_data(assets[selected_asset])

fig_detail = go.Figure(data=[go.Candlestick(
    x=detail_df.index,
    open=detail_df['Open'].iloc[:, 0],
    high=detail_df['High'].iloc[:, 0],
    low=detail_df['Low'].iloc[:, 0],
    close=detail_df['Close'].iloc[:, 0],
    increasing_line_color=ACCENT_COLOR, 
    decreasing_line_color='#FF4B4B'
)])

fig_detail.update_layout(
    template="plotly_dark",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_rangeslider_visible=False,
    font=dict(color=TEXT_COLOR)
)

st.plotly_chart(fig_detail, use_container_width=True)

st.caption("Data leveres av Yahoo Finance API. Bakgrunnsfarge: BI Mørkeblå (#00244E).")
