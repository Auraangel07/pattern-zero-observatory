# ═══════════════════════════════════════════
# PATTERN ZERO — MARKET OBSERVATORY
# "The face of the ecosystem. Live. Beautiful."
# ═══════════════════════════════════════════

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils.db import run_query
from utils.sidebar import render_sidebar
from utils.theme import apply_theme, get_chart_layout
# ───────────────────────────────────────────
# PAGE CONFIG
# ───────────────────────────────────────────
st.set_page_config(
    page_title="Pattern Zero — Market Observatory",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

# ───────────────────────────────────────────
# HEADER
# ───────────────────────────────────────────
col_title, col_status = st.columns([4, 1])
with col_title:
    st.markdown('<p class="main-title">PATTERN ZERO</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">MARKET OBSERVATORY · "Complexity is not chaos. It is unread data."</p>', unsafe_allow_html=True)
with col_status:
    st.markdown(
        f'<div style="text-align:right; padding-top:20px;">'
        f'<span class="status-pill status-live">● LIVE</span><br>'
        f'<span style="color:#666; font-size:0.75rem; font-family:DM Mono,monospace;">{datetime.now().strftime("%H:%M:%S UTC")}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

st.markdown("---")

# ───────────────────────────────────────────
# OVERVIEW — Executive Summary Row
# ───────────────────────────────────────────
@st.cache_data(ttl=300)
def get_overview_stats():
    symbols = run_query("SELECT COUNT(*) as n FROM symbols_registry")
    stocks = run_query("SELECT COUNT(*) as n FROM stock_prices")
    macro = run_query("SELECT COUNT(*) as n FROM macro_indicators")
    news = run_query("SELECT COUNT(*) as n FROM news_sentiment")
    filings = run_query("SELECT COUNT(*) as n FROM sec_filings")
    health = run_query("""
        SELECT COUNT(*) FILTER (WHERE status = 'SUCCESS') as healthy,
               COUNT(*) as total
        FROM (
            SELECT DISTINCT ON (pipeline_name) pipeline_name, status
            FROM pipeline_logs
            ORDER BY pipeline_name, started_at DESC
        ) latest
    """)
    return symbols, stocks, macro, news, filings, health

symbols_df, stocks_df, macro_df, news_df, filings_df, health_df = get_overview_stats()

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.metric("Symbols", int(symbols_df['n'][0]))
with k2:
    st.metric("Price Records", f"{int(stocks_df['n'][0]):,}")
with k3:
    st.metric("Macro Records", f"{int(macro_df['n'][0]):,}")
with k4:
    st.metric("News Articles", f"{int(news_df['n'][0]):,}")
with k5:
    st.metric("SEC Filings", f"{int(filings_df['n'][0]):,}")
with k6:
    healthy = int(health_df['healthy'][0])
    total = int(health_df['total'][0])
    st.metric("Pipelines Healthy", f"{healthy}/{total}")

st.markdown("---")

# ───────────────────────────────────────────
# FILTER BAR
# ───────────────────────────────────────────
st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns([2, 2, 1])
with fc1:
    date_range = st.date_input("Date Range", value=(), key="global_date_filter")
with fc2:
    asset_filter = st.multiselect(
        "Asset Classes",
        ["Equities", "ETFs", "Crypto"],
        default=["Equities", "ETFs", "Crypto"],
        key="global_asset_filter"
    )
with fc3:
    st.write("")
    st.button("🔄 Refresh", key="refresh_btn")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
# ───────────────────────────────────────────
# LIVE MARKET SNAPSHOT
# ───────────────────────────────────────────
st.markdown("### Live Market Snapshot")

@st.cache_data(ttl=300)
def get_latest_prices():
    query = """
        SELECT DISTINCT ON (symbol)
            symbol, time, open, high, low, close, volume
        FROM stock_prices
        ORDER BY symbol, time DESC
    """
    return run_query(query)

try:
    latest = get_latest_prices()

    if not latest.empty:
        # Separate crypto from equities for cleaner grouping
        crypto_mask = latest['symbol'].str.contains('-USD')
        equities = latest[~crypto_mask].sort_values('symbol')
        crypto = latest[crypto_mask].sort_values('symbol')

        tab1, tab2 = st.tabs(["Equities & ETFs", "Crypto"])

        def render_metrics(df, currency_symbol="$"):
            cols = st.columns(5)
            for idx, (_, row) in enumerate(df.iterrows()):
                col = cols[idx % 5]
                with col:
                    change_pct = ((row['close'] - row['open']) / row['open']) * 100 if row['open'] else 0
                    st.metric(
                        label=row['symbol'],
                        value=f"{currency_symbol}{row['close']:,.2f}",
                        delta=f"{change_pct:.2f}%"
                    )

        with tab1:
            render_metrics(equities)
        with tab2:
            render_metrics(crypto)

    else:
        st.warning("No stock data found yet. Has the ingestion pipeline run?")

except Exception as e:
    st.error(f"Could not connect to database: {e}")

st.markdown("---")

# ───────────────────────────────────────────
# PRICE HISTORY CHART
# ───────────────────────────────────────────
st.markdown("### Price History")

try:
    all_symbols = sorted(latest['symbol'].tolist()) if not latest.empty else []

    if all_symbols:
        c1, c2 = st.columns([1, 3])
        with c1:
            selected_symbol = st.selectbox("Symbol", all_symbols)
            days = st.slider("Days of history", 7, 90, 30)

        @st.cache_data(ttl=300)
        def get_history(symbol, days):
            query = """
                SELECT time, open, high, low, close, volume
                FROM stock_prices
                WHERE symbol = :symbol
                  AND time >= NOW() - (:days || ' days')::interval
                ORDER BY time ASC
            """
            return run_query(query, {"symbol": symbol, "days": days})

        history = get_history(selected_symbol, days)

        with c2:
            if not history.empty:
                fig = go.Figure(data=[go.Candlestick(
                    x=history['time'],
                    open=history['open'],
                    high=history['high'],
                    low=history['low'],
                    close=history['close'],
                    increasing_line_color="#D4AF37",
                    decreasing_line_color="#8B2E2E",
                    name=selected_symbol
                )])

                fig.update_layout(**get_chart_layout(f"{selected_symbol} — Last {days} Days"))
                fig.update_layout(xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, width='stretch')
            else:
                st.info(f"No history found for {selected_symbol}")

except Exception as e:
    st.error(f"Error loading chart: {e}")

st.markdown("---")

render_sidebar()