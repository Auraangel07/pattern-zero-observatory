# ═══════════════════════════════════════════
# PATTERN ZERO — MARKET OBSERVATORY
# News & Filings — Project 03 surface
# ═══════════════════════════════════════════

import streamlit as st
from utils.db import run_query
from utils.theme import apply_theme
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="Pattern Zero — News & Filings",
    layout="wide"
)

apply_theme()

st.markdown('<p class="page-title">News & Filings</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">ALTERNATIVE DATA · WHAT\'S BEING SAID, WHAT\'S BEING DISCLOSED</p>', unsafe_allow_html=True)
st.markdown("---")

# ───────────────────────────────────────────
# SYMBOL FILTER
# ───────────────────────────────────────────
@st.cache_data(ttl=300)
def get_tracked_symbols():
    query = """
        SELECT DISTINCT symbols[1] as symbol
        FROM news_sentiment
        WHERE symbols IS NOT NULL
        UNION
        SELECT DISTINCT symbol FROM sec_filings
        ORDER BY 1
    """
    return run_query(query)

symbols_df = get_tracked_symbols()
symbol_list = symbols_df['symbol'].dropna().tolist() if not symbols_df.empty else []

selected = st.selectbox("Filter by symbol", ["All"] + symbol_list)

st.markdown("---")

col_news, col_filings = st.columns(2)

# ───────────────────────────────────────────
# NEWS PANEL
# ───────────────────────────────────────────
with col_news:
    st.markdown("### Recent Headlines")

    @st.cache_data(ttl=300)
    def get_news(symbol_filter):
        if symbol_filter == "All":
            query = """
                SELECT time, headline, source, url, symbols
                FROM news_sentiment
                ORDER BY time DESC
                LIMIT 20
            """
            return run_query(query)
        else:
            query = """
                SELECT time, headline, source, url, symbols
                FROM news_sentiment
                WHERE :symbol = ANY(symbols)
                ORDER BY time DESC
                LIMIT 20
            """
            return run_query(query, {"symbol": symbol_filter})

    news_df = get_news(selected)

    if not news_df.empty:
        for _, row in news_df.iterrows():
            st.markdown(
                f"**[{row['headline']}]({row['url']})**  \n"
                f"<span style='color:#888; font-size:0.8rem;'>{row['source']} · {row['time']}</span>",
                unsafe_allow_html=True
            )
            st.markdown("")
    else:
        st.info("No news found for this filter.")

# ───────────────────────────────────────────
# FILINGS PANEL
# ───────────────────────────────────────────
with col_filings:
    st.markdown("### Recent SEC Filings")

    @st.cache_data(ttl=300)
    def get_filings(symbol_filter):
        if symbol_filter == "All":
            query = """
                SELECT symbol, company_name, filing_type,
                       filing_date, url
                FROM sec_filings
                ORDER BY filing_date DESC
                LIMIT 20
            """
            return run_query(query)
        else:
            query = """
                SELECT symbol, company_name, filing_type,
                       filing_date, url
                FROM sec_filings
                WHERE symbol = :symbol
                ORDER BY filing_date DESC
                LIMIT 20
            """
            return run_query(query, {"symbol": symbol_filter})

    filings_df = get_filings(selected)

    if not filings_df.empty:
        for _, row in filings_df.iterrows():
            st.markdown(
                f"**[{row['filing_type']} — {row['company_name']}]({row['url']})**  \n"
                f"<span style='color:#888; font-size:0.8rem;'>{row['symbol']} · {row['filing_date']}</span>",
                unsafe_allow_html=True
            )
            st.markdown("")
    else:
        st.info("No filings found for this filter.")

st.markdown("---")
st.caption("Pattern Zero · Module I: STRATUM · Project 03")
render_sidebar()