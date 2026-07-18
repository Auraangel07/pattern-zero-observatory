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
from utils.theme import apply_theme
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

# ───────────────────────────────────────────
# OVERVIEW ROW — Executive Summary
# ───────────────────────────────────────────
st.markdown('<p class="subtitle" style="margin-bottom:10px;">SYSTEM OVERVIEW</p>', unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_overview_stats():
    symbols_query = "SELECT COUNT(DISTINCT symbol) as cnt FROM stock_prices"
    records_query = "SELECT COUNT(*) as cnt FROM stock_prices"
    pipelines_query = """
        SELECT COUNT(*) FILTER (WHERE status = 'SUCCESS') as success,
               COUNT(*) as total
        FROM (
            SELECT DISTINCT ON (pipeline_name) pipeline_name, status
            FROM pipeline_logs
            ORDER BY pipeline_name, started_at DESC
        ) latest
    """
    symbols_count = run_query(symbols_query)['cnt'].iloc[0]
    records_count = run_query(records_query)['cnt'].iloc[0]
    pipeline_health = run_query(pipelines_query)
    return symbols_count, records_count, pipeline_health

try:
    symbols_count, records_count, pipeline_health = get_overview_stats()
    success = pipeline_health['success'].iloc[0]
    total = pipeline_health['total'].iloc[0]

    st.markdown('<div class="overview-row">', unsafe_allow_html=True)
    o1, o2, o3, o4 = st.columns(4)
    o1.metric("Symbols Tracked", symbols_count)
    o2.metric("Total Records", f"{records_count:,}")
    o3.metric("Pipelines Healthy", f"{success}/{total}")
    o4.metric("Data Source", "Yahoo Finance")
    st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Overview unavailable: {e}")
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

                fig.update_layout(
                    title=f"{selected_symbol} — Last {days} Days",
                    xaxis_title=None,
                    yaxis_title="Price",
                    template="plotly_dark",
                    height=450,
                    paper_bgcolor="#0A0A0A",
                    plot_bgcolor="#0A0A0A",
                    font=dict(family="DM Mono, monospace", color="#E8E8E8"),
                    xaxis_rangeslider_visible=False,
                    margin=dict(t=50, b=20, l=20, r=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"No history found for {selected_symbol}")

except Exception as e:
    st.error(f"Error loading chart: {e}")

st.markdown("---")

render_sidebar()