# Pattern Zero — Market Observatory

**Project 02 of Module I: STRATUM** — a live, multi-page dashboard visualizing Pattern Zero's automated financial data pipeline.

> *"Complexity is not chaos. It is unread data."*

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?logo=plotly&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/TimescaleDB-PostgreSQL-4169E1?logo=postgresql&logoColor=white)

---

## What it does

The Observatory is the visual face of STRATUM — it reads live from the same TimescaleDB that STRATUM's Airflow pipelines fill automatically, with zero duplicate data logic. Three pages:

- **🗺️ Home** — system overview (symbols tracked, total records, pipeline health), live market snapshot for equities/ETFs/crypto with real-time % change, and interactive candlestick history charts
- **🏛️ Macro Indicators** — latest macroeconomic readings (GDP, CPI, Fed funds rate, Treasury yields) with historical trend charts
- **🛰️ Pipeline Health** — full audit trail of every ingestion run, filterable by pipeline, with expandable error details for any failures

## Screenshots

### Home — Live Market Snapshot
![Home Dashboard](docs/screenshots/home.png)

### Macro Indicators
![Macro Indicators](docs/screenshots/macro.png)

### Pipeline Health
![Pipeline Health](docs/screenshots/pipeline.png)

## Tech stack

- **Streamlit** — multi-page app framework
- **Plotly** — interactive candlestick and line charts
- **SQLAlchemy** — read-only connection into STRATUM's TimescaleDB
- Custom dark theme (Obsidian/Gold) matching Pattern Zero's brand identity

## Architecture
STRATUM's TimescaleDB (read-only)
│
▼
SQLAlchemy queries
(utils/db.py — shared connection)
│
▼
Streamlit multi-page app
app.py · pages/Macro · pages/Pipeline
│
▼
Plotly visualizations

The Observatory never writes to the database — strictly read-only, keeping it fully decoupled from ingestion.

## Running it locally

```bash
git clone https://github.com/Auraangel07/pattern-zero-observatory.git
cd pattern-zero-observatory
cp .env.example .env   # point at your running STRATUM database
pip install -r requirements.txt
streamlit run app.py
```

Requires STRATUM's TimescaleDB to be running (`docker-compose up -d` in the STRATUM repo) — the Observatory reads from it but doesn't manage it.

## Project Status

Project 02 of Module I. Complete — three pages, live data, consistent theming.

## Roadmap

Next: Project 03 — Alternative Data Pipeline, then Module I is sealed and Pattern Zero moves to Module II — THE CALCULUS.

---

*Built as part of Pattern Zero — an independent financial AI research project.*
