# ═══════════════════════════════════════════
# PATTERN ZERO — Shared Sidebar Component
# ═══════════════════════════════════════════

import streamlit as st
from utils.db import run_query

def render_sidebar():
    with st.sidebar:
        st.markdown('<p style="font-family:Cormorant Garamond,serif; font-size:1.6rem; color:#D4AF37;">System Status</p>', unsafe_allow_html=True)
        st.markdown("---")

        try:
            @st.cache_data(ttl=60)
            def get_pipeline_status():
                query = """
                    SELECT DISTINCT ON (pipeline_name)
                        pipeline_name, status,
                        records_inserted, completed_at
                    FROM pipeline_logs
                    ORDER BY pipeline_name, started_at DESC
                """
                return run_query(query)

            status_df = get_pipeline_status()

            if not status_df.empty:
                for _, row in status_df.iterrows():
                    icon = "🟢" if row['status'] == 'SUCCESS' else "🟡"
                    st.markdown(
                        f"{icon} **{row['pipeline_name']}**  \n"
                        f"`{row['records_inserted']} records`  \n"
                        f"<span style='color:#666; font-size:0.75rem;'>{row['completed_at']}</span>",
                        unsafe_allow_html=True
                    )
                    st.markdown("")
            else:
                st.info("No pipeline runs logged yet")

        except Exception as e:
            st.error(f"Status unavailable: {e}")

        st.markdown("---")
        st.caption("Pattern Zero · Module I: STRATUM · Project 02")