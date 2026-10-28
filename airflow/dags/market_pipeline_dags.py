import sys
import pandas as pd

if '/opt/airflow/' not in sys.path:
    sys.path.insert(0, '/opt/airflow')

from airflow.sdk import DAG, task
from datetime import datetime, timedelta

from src.ingest.source_a import ingest_source_a
from src.ingest.source_b import ingest_source_b
from src.transform.clean import clean_data
from src.transform.merge import merge_data
from src.analytics.build_analytics import build_star_schema
from src.common.config import SOURCE_A_RAW_PATH, SOURCE_B_RAW_PATH, DB_PATH

import duckdb
CLEAN_OUTPUT_PATH = "data/processed/prices_clean_dag.parquet"
JOINED_OUTPUT_PATH = "data/processed/prices_with_rainfall.parquet"

with DAG(
    dag_id = "market_pipeline",
    schedule = "@daily",
    start_date = datetime(2026, 10, 2),
    catchup = False,
):

    # 1. Ingestion: Aggressive retries + exponential backoff for flaky external sources/networks
    @task(retries=4, retry_delay=timedelta(seconds=30), retry_exponential_backoff=True, max_retry_delay=timedelta(minutes=10))
    def acquire_a():
        df = ingest_source_a(SOURCE_A_RAW_PATH)
        return {"path":SOURCE_A_RAW_PATH, "rows": len(df)}

    @task(retries=4, retry_delay=timedelta(seconds=30), retry_exponential_backoff=True, max_retry_delay=timedelta(minutes=10))
    def acquire_b():
        df = ingest_source_b(SOURCE_B_RAW_PATH)
        return {"path":SOURCE_B_RAW_PATH, "rows": len(df)}

    # 2. Transformation: Moderate retries for local file IO / pandas operations
    @task(retries=2, retry_delay=timedelta(minutes=2))
    def clean(acquire_a_result: dict):
        clean_df, log = clean_data(acquire_a_result["path"])
        clean_df.to_parquet(CLEAN_OUTPUT_PATH, index=False)
        return {"path": CLEAN_OUTPUT_PATH, "rows": len(clean_df), "rules_triggered": len(log)}

    @task(retries=2, retry_delay=timedelta(minutes=2))
    def merge(clean_result: dict, acquire_b_result: dict):
        clean_df = pd.read_parquet(clean_result["path"])
        rainfall = ingest_source_b(acquire_b_result["path"])

        merged_data = merge_data(clean_df, rainfall)
        merged_data.to_parquet(JOINED_OUTPUT_PATH, index=False)

        return {"path": JOINED_OUTPUT_PATH, "rows": len(merged_data)}

    # 3. Storage / Database: Low retries (Ensure build_star_schema is idempotent!)
    @task(retries=1, retry_delay=timedelta(minutes=1))
    def store(merge_result: dict):
        build_star_schema()
        return {"Status:": "Star schema successfully built and stored."}

    # 4. Reporting: Safe to retry, light read-only check
    @task(retries=2, retry_delay=timedelta(seconds=15))
    def report():
        duckdb_conn = duckdb.connect(DB_PATH)
        row_count = duckdb_conn.sql("SELECT COUNT(*) FROM fact_price_observation").fetchone()[0]
        duckdb_conn.close()

        return {"run_date": "{{ ds }}", "fact_table_row_count": row_count}


    # Dependencies wiring
    a_res = acquire_a()
    b_res = acquire_b()

    clean_res = clean(a_res)
    merge_res = merge(clean_res, b_res)
    store_res = store(merge_res)

    store_res >> report()