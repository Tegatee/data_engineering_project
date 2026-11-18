"""Create the Snowflake raw tables and load raw_data/*.csv into them."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

ROOT = Path(__file__).resolve().parent.parent

print(os.getenv("SNOWFLAKE_ACCOUNT"))

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    role= "ACCOUNTADMIN",
)

try:
    cur = conn.cursor()

    ddl = (ROOT / "sql" / "00_raw_setup.sql").read_text()
    for stmt in [s.strip() for s in ddl.split(";") if s.strip()]:
        cur.execute(stmt)

    cur.execute("use warehouse BLUKOLA_WH")
    cur.execute("use database BLUKOLA")
    cur.execute("use schema raw")

    TABLES = {
        "customers": ["created_at"],
        "products": [],
        "orders": ["ordered_at", "_loaded_at"],
        "order_items": [],
        "payments": ["paid_at"],
    }

    for table, date_cols in TABLES.items():
        df = pd.read_csv(ROOT / "raw_data" / f"{table}.csv", parse_dates=date_cols)
        df.columns = [c.upper() for c in df.columns]
        cur.execute(f"truncate table {table}")
        ok, _, nrows, _ = write_pandas(conn, df, table.upper(), database="BLUKOLA", schema="RAW",
                                    use_logical_type=True)
        print(f"{table}: loaded {nrows} rows (ok={ok})")

    for table in TABLES:
        cur.execute(f"select count(*) from {table}")
        print(f"{table}: {cur.fetchone()[0]} rows in Snowflake")
finally:
    cur.close()
    conn.close()
