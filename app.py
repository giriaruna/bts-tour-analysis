import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BTS Tour Audit", layout="wide")

st.title("💜 BTS: The Quantum Leap (2018 vs 2026)")
st.sidebar.markdown("### Engineering Dashboard")
st.sidebar.info("Comparing Love Yourself (Baseline) vs. Arirang (Projected)")

# Load Data
try:
    # 1. Load Economic Data from tour_processor.py
    econ = pd.read_csv('tour_economics.csv')
    
    # 2. Load Signal Data from spotify_fetcher.py
    signals = pd.read_csv('spotify_signals.csv')

    # Visual 1: Economic Growth
    st.header("1. Global Economic Impact")
    fig_econ = px.bar(
        econ, 
        x='city', 
        y='revenue_usd', 
        color='era', 
        barmode='group',
        color_discrete_map={'LY_2018': '#8E44AD', 'ARIRANG_2026': '#2ECC71'},
        title="Revenue Comparison: 2018 Actual vs. 2026 Projected (USD)"
    )
    st.plotly_chart(fig_econ, use_container_width=True)

    # Visual 2: Sonic Profile
    st.header("2. Sonic Engineering Analysis")
    fig_sonic = px.box(
        signals, 
        x='era', 
        y='energy', 
        color='era',
        points="all",
        title="Audio Signal Energy: Is the 'Arirang' sound engineered for larger stadiums?"
    )
    st.plotly_chart(fig_sonic, use_container_width=True)

    # Data Peer Review Section (For your teammates)
    with st.expander(" View Raw Data Pipeline"):
        col1, col2 = st.columns(2)
        col1.write("Economic Data (Scraped)")
        col1.dataframe(econ.head())
        col2.write("Signal Data (API)")
        col2.dataframe(signals.head())

except FileNotFoundError as e:
    st.error(f"Missing Data File: {e.filename}")
    st.warning("Please run 'spotify_fetcher.py' and 'tour_processor.py' first!")
