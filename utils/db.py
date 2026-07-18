# ═══════════════════════════════════════════
# PATTERN ZERO — Observatory
# Shared database connection
# ═══════════════════════════════════════════

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    connection_string = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
    return create_engine(connection_string)

def run_query(query: str, params: dict = None) -> pd.DataFrame:
    """
    Runs a SQL query and returns a pandas DataFrame.
    Every dashboard component uses this.
    """
    engine = get_engine()
    with engine.begin() as conn:
        result = pd.read_sql(text(query), conn, params=params)
    return result