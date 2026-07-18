# ═══════════════════════════════════════════
# PATTERN ZERO — Macro Indicators
# ═══════════════════════════════════════════

import streamlit as st
import plotly.graph_objects as go
from utils.db import run_query
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="Pattern Zero — Macro Indicators",
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()

st.markdown('<p class="page-title">Macro Indicators</p>', unsafe_allow_html=True)
st.caption("GDP · Inflation · Interest Rates · Employment — the big picture behind every price move.")
st.markdown("---")

@st.cache_data(ttl=600)
def get_indicators():
    query = """
        SELECT DISTINCT indicator, country
        FROM macro_indicators
        ORDER BY indicator
    """
    return run_query(query)

@st.cache_data(ttl=600)
def get_latest_snapshot():
    query = """
        SELECT DISTINCT ON (indicator, country)
            indicator, country, time, value, unit
        FROM macro_indicators
        ORDER BY indicator, country, time DESC
    """
    return run_query(query)

try:
    snapshot = get_latest_snapshot()

    if not snapshot.empty:
        st.markdown("### Latest Readings")
        cols = st.columns(4)
        for idx, (_, row) in enumerate(snapshot.iterrows()):
            col = cols[idx % 4]
            with col:
                st.metric(
                    label=f"{row['indicator']} ({row['country']})",
                    value=f"{row['value']:.2f} {row['unit'] or ''}"
                )

        st.markdown("---")
        st.markdown("### Historical Trend")

        indicators_df = get_indicators()
        indicator_options = indicators_df['indicator'].tolist()

        selected_indicator = st.selectbox("Select indicator", indicator_options)
        selected_country = st.selectbox(
            "Country",
            indicators_df[indicators_df['indicator'] == selected_indicator]['country'].tolist()
        )

        @st.cache_data(ttl=600)
        def get_indicator_history(indicator, country):
            query = """
                SELECT time, value
                FROM macro_indicators
                WHERE indicator = :indicator AND country = :country
                ORDER BY time ASC
            """
            return run_query(query, {"indicator": indicator, "country": country})

        history = get_indicator_history(selected_indicator, selected_country)

        if not history.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=history['time'],
                y=history['value'],
                mode='lines+markers',
                line=dict(color="#D4AF37", width=2),
                marker=dict(size=5, color="#F4E5B2"),
                fill='tozeroy',
                fillcolor='rgba(212, 175, 55, 0.08)'
            ))
            fig.update_layout(
                title=f"{selected_indicator} — {selected_country}",
                template="plotly_dark",
                paper_bgcolor="#0A0A0A",
                plot_bgcolor="#0A0A0A",
                font=dict(family="DM Mono, monospace", color="#E8E8E8"),
                height=450,
                margin=dict(t=50, b=20, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No historical data for this selection")
    else:
        st.warning("No macro data found. Has stratum_macro run yet?")

except Exception as e:
    st.error(f"Error loading macro data: {e}")

render_sidebar()