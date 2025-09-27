import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="📈 Nifty Stocks Explorer", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Nifty_Stocks.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Title
st.title("Nifty Stocks Explorer")

# Sidebar filters
st.sidebar.header("🔎 Filters")

# Category selection
categories = df["Category"].unique()
category = st.sidebar.selectbox("Select Category", categories)

df_cat = df[df["Category"] == category]

# Symbol selection
symbols = df_cat["Symbol"].unique()
symbol = st.sidebar.selectbox("Select Symbol", symbols)

df_symbol = df_cat[df_cat["Symbol"] == symbol].sort_values("Date")

# Date range filter
min_date, max_date = df_symbol["Date"].min(), df_symbol["Date"].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

if len(date_range) == 2:
    df_symbol = df_symbol[(df_symbol["Date"] >= pd.to_datetime(date_range[0])) &
                          (df_symbol["Date"] <= pd.to_datetime(date_range[1]))]

# Chart type
chart_type = st.sidebar.radio("Chart Type", ["Line", "Area", "Candlestick"])

# Indicators
show_sma50 = st.sidebar.checkbox("Show SMA 50")
show_sma200 = st.sidebar.checkbox("Show SMA 200")

# Compute indicators
if show_sma50:
    df_symbol["SMA_50"] = df_symbol["Close"].rolling(window=50).mean()
if show_sma200:
    df_symbol["SMA_200"] = df_symbol["Close"].rolling(window=200).mean()

# Plotting
if chart_type in ["Line", "Area"]:
    fig = px.line(df_symbol, x="Date", y="Close", title=f"{symbol} Closing Price")
    if chart_type == "Area":
        fig = px.area(df_symbol, x="Date", y="Close", title=f"{symbol} Closing Price")
    
    # Add indicators
    if show_sma50:
        fig.add_scatter(x=df_symbol["Date"], y=df_symbol["SMA_50"], mode="lines", name="SMA 50")
    if show_sma200:
        fig.add_scatter(x=df_symbol["Date"], y=df_symbol["SMA_200"], mode="lines", name="SMA 200")

elif chart_type == "Candlestick":
    fig = go.Figure(data=[go.Candlestick(x=df_symbol["Date"],
                                         open=df_symbol["Open"],
                                         high=df_symbol["High"],
                                         low=df_symbol["Low"],
                                         close=df_symbol["Close"])])
    fig.update_layout(title=f"{symbol} Candlestick Chart", xaxis_rangeslider_visible=False)

# Show chart
st.plotly_chart(fig, use_container_width=True)
