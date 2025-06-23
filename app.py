# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

# Set page configuration
st.set_page_config(page_title="Adani Ports Stock Analysis", layout="wide")

st.title("📈 ADANIPORTS Stock Technical Analysis")
st.markdown("This app performs technical analysis of **Adani Ports (ADANIPORTS.NS)** using Moving Averages, RSI, MACD, and Bollinger Bands.")

# Fetch Data
@st.cache_data
def load_data():
    df = yf.download('ADANIPORTS.NS', start='2020-01-01', end='2025-01-01')
    df.dropna(inplace=True)
    return df

df = load_data()

# Calculate indicators
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()

rsi = RSIIndicator(close=df['Close'], window=14)
df['RSI'] = rsi.rsi()

macd = MACD(close=df['Close'])
df['MACD'] = macd.macd()
df['MACD_Signal'] = macd.macd_signal()

bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
df['BB_High'] = bb.bollinger_hband()
df['BB_Low'] = bb.bollinger_lband()

df['Daily Return'] = df['Close'].pct_change()
df['Cumulative Return'] = (1 + df['Daily Return']).cumprod()

# Sidebar
st.sidebar.header("📌 Options")
show_ma = st.sidebar.checkbox("Show Moving Averages & Bollinger Bands", True)
show_rsi = st.sidebar.checkbox("Show RSI", True)
show_macd = st.sidebar.checkbox("Show MACD", True)
show_returns = st.sidebar.checkbox("Show Returns", True)

# Charts
if show_ma:
    st.subheader("Close Price with Moving Averages & Bollinger Bands")
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df['Close'], label='Close', color='blue')
    ax.plot(df['MA20'], label='MA20', color='orange')
    ax.plot(df['MA50'], label='MA50', color='green')
    ax.plot(df['BB_High'], label='BB High', linestyle='--', alpha=0.4)
    ax.plot(df['BB_Low'], label='BB Low', linestyle='--', alpha=0.4)
    ax.fill_between(df.index, df['BB_Low'], df['BB_High'], color='gray', alpha=0.1)
    ax.set_title('ADANIPORTS - Price with MA & Bollinger Bands')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

if show_rsi:
    st.subheader("Relative Strength Index (RSI)")
    fig, ax = plt.subplots(figsize=(14, 3))
    ax.plot(df['RSI'], label='RSI', color='purple')
    ax.axhline(70, color='red', linestyle='--')
    ax.axhline(30, color='green', linestyle='--')
    ax.set_title('RSI - Overbought/ Oversold Zones')
    ax.grid(True)
    st.pyplot(fig)

if show_macd:
    st.subheader("MACD & Signal Line")
    fig, ax = plt.subplots(figsize=(14, 3))
    ax.plot(df['MACD'], label='MACD', color='blue')
    ax.plot(df['MACD_Signal'], label='Signal Line', color='red')
    ax.legend()
    ax.grid(True)
    ax.set_title('MACD vs Signal')
    st.pyplot(fig)

if show_returns:
    st.subheader("Cumulative Return of ADANIPORTS")
    fig, ax = plt.subplots(figsize=(14, 3))
    ax.plot(df['Cumulative Return'], color='green')
    ax.set_title('Cumulative Return')
    ax.grid(True)
    st.pyplot(fig)

    st.write("📊 **Average Daily Return:**", round(df['Daily Return'].mean(), 4))
    st.write("📊 **Volatility (Standard Deviation):**", round(df['Daily Return'].std(), 4))
