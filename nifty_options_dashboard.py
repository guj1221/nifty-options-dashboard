
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Simulate 30 days of Nifty price data
np.random.seed(42)
days = pd.date_range(end=pd.Timestamp.today(), periods=30)
price = np.cumsum(np.random.randn(30)) + 19500  # Starting around 19500

df = pd.DataFrame({'Date': days, 'Close': price})
df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()

# Supertrend (simplified logic)
df['Supertrend'] = np.where(df['Close'] > df['EMA20'], 'bull', 'bear')

# Mock PCR and VIX values
pcr = 0.95
vix = 14.5
price_latest = df['Close'].iloc[-1]
ema20_latest = df['EMA20'].iloc[-1]
supertrend_latest = df['Supertrend'].iloc[-1]

# Generate signal
if pcr < 1 and price_latest > ema20_latest and supertrend_latest == 'bull':
    signal = "✅ Buy CALL"
elif pcr > 1 and price_latest < ema20_latest and supertrend_latest == 'bear':
    signal = "🔻 Buy PUT"
else:
    signal = "⚠️ No clear trend / Sideways"

# Streamlit App Display
st.set_page_config(page_title="Nifty Options Signal", layout="centered")
st.title("📊 Nifty Options Dashboard")

st.markdown(f"### 🔔 Trade Signal: {signal}")
st.metric("Put/Call Ratio (PCR)", f"{pcr:.2f}")
st.metric("India VIX", f"{vix:.2f}")
st.line_chart(df.set_index("Date")[['Close', 'EMA20', 'EMA50']])
