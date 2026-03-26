import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BTS Tour Audit", layout="wide")

st.title("💜 BTS: The Quantum Leap (2018 vs 2026)")
st.sidebar.markdown("### Engineering Dashboard")
st.sidebar.info("Comparing Love Yourself (Baseline) vs. Arirang (Projected)")

df = pd.read
