# ═══════════════════════════════════════════
# PATTERN ZERO — Shared Theme / CSS
# One design system, imported on every page
# ═══════════════════════════════════════════

import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Mono:wght@400;500&display=swap');

        /* ── Typography ── */
        .main-title {
            font-family: 'Cormorant Garamond', serif;
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(90deg, #D4AF37, #F4E5B2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
        }
        .page-title {
            font-family: 'Cormorant Garamond', serif;
            font-size: 2.4rem;
            font-weight: 700;
            color: #D4AF37;
            margin-bottom: 0;
        }
        .subtitle {
            font-family: 'DM Mono', monospace;
            color: #888;
            font-size: 0.9rem;
            letter-spacing: 1px;
        }

        /* ── KPI Cards ── */
        div[data-testid="stMetric"] {
            background: linear-gradient(145deg, #161616, #0D0D0D);
            border: 1px solid #262626;
            border-radius: 14px;
            padding: 18px 16px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.45);
            transition: all 0.2s ease;
        }
        div[data-testid="stMetric"]:hover {
            border: 1px solid #D4AF37;
            box-shadow: 0 6px 20px rgba(212,175,55,0.15);
            transform: translateY(-2px);
        }
        div[data-testid="stMetricLabel"] {
            font-family: 'DM Mono', monospace;
            font-size: 0.8rem;
            color: #999;
            letter-spacing: 0.5px;
        }
        div[data-testid="stMetricValue"] {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.9rem;
        }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background-color: #0B0B0B;
            border-right: 1px solid #262626;
        }

        /* ── Status pill ── */
        .status-pill {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-family: 'DM Mono', monospace;
            background: rgba(212, 175, 55, 0.12);
            color: #D4AF37;
            border: 1px solid #D4AF37;
        }

        /* ── Filter bar container ── */
        .filter-bar {
            background: #111111;
            border: 1px solid #262626;
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 18px;
        }

        /* ── Tabs ── */
        button[data-baseweb="tab"] {
            font-family: 'DM Mono', monospace;
        }

        /* ── Dataframe ── */
        div[data-testid="stDataFrame"] {
            border: 1px solid #262626;
            border-radius: 10px;
        }

        hr {
            border-color: #262626;
        }
        
        /* ── Overview / Summary cards — distinguished with top accent ── */
        .overview-row div[data-testid="stMetric"] {
            border-top: 2px solid #D4AF37;
            background: linear-gradient(180deg, rgba(212,175,55,0.06), #0D0D0D 40%);
        }
        .overview-row div[data-testid="stMetricValue"] {
            color: #F4E5B2;
        }
    </style>
    """, unsafe_allow_html=True)