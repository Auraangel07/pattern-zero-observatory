# ═══════════════════════════════════════════
# PATTERN ZERO — Pipeline Health
# ═══════════════════════════════════════════

import streamlit as st
from utils.db import run_query
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="Pattern Zero — Pipeline Health",
    layout="wide"
)

from utils.theme import apply_theme
apply_theme()
st.markdown('<p class="page-title"> Pipeline Health</p>', unsafe_allow_html=True)
st.caption("Full audit trail of every automated ingestion run — this is the infrastructure, made visible.")
st.markdown("---")

@st.cache_data(ttl=60)
def get_all_logs():
    query = """
        SELECT pipeline_name, status, records_fetched,
               records_inserted, error_message,
               started_at, completed_at
        FROM pipeline_logs
        ORDER BY started_at DESC
        LIMIT 100
    """
    return run_query(query)

try:
    logs = get_all_logs()

    if not logs.empty:
        # Summary metrics
        c1, c2, c3, c4 = st.columns(4)
        total_runs = len(logs)
        success_runs = len(logs[logs['status'] == 'SUCCESS'])
        failed_runs = len(logs[logs['status'] != 'SUCCESS'])
        total_records = logs['records_inserted'].sum()

        c1.metric("Total Runs (last 100)", total_runs)
        c2.metric("Successful", success_runs)
        c3.metric("Failed / Partial", failed_runs)
        c4.metric("Records Inserted", f"{total_records:,}")

        st.markdown("---")

        # Filter
        pipeline_filter = st.selectbox(
            "Filter by pipeline",
            ["All"] + sorted(logs['pipeline_name'].unique().tolist())
        )

        display_logs = logs if pipeline_filter == "All" else logs[logs['pipeline_name'] == pipeline_filter]

        st.markdown(f"### Run History ({len(display_logs)} runs)")

        st.dataframe(
            display_logs[[
                'pipeline_name', 'status', 'records_fetched',
                'records_inserted', 'started_at', 'completed_at'
            ]],
            use_container_width=True,
            height=500
        )

        # Show errors if any
        errors = display_logs[display_logs['error_message'].notna()]
        if not errors.empty:
            st.markdown("---")
            st.markdown("### ⚠️ Error Details")
            for _, row in errors.iterrows():
                with st.expander(f"{row['pipeline_name']} — {row['started_at']}"):
                    st.code(row['error_message'])
    else:
        st.info("No pipeline runs logged yet")

except Exception as e:
    st.error(f"Error loading pipeline logs: {e}")

render_sidebar()