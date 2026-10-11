import sys

if '/opt/airflow/' not in sys.path:
    sys.path.insert(0, '/opt/airflow')

from airflow.sdk import DAG, task
from datetime import datetime

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

    @task
    def acquire_a():
        df = ingest_source_a(SOURCE_A_RAW_PATH)
        return {"path":SOURCE_A_RAW_PATH, "rows": len(df)}

    @task
    def acquire_b():
        df = ingest_source_b(SOURCE_B_RAW_PATH)
        return {"path":SOURCE_B_RAW_PATH, "rows": len(df)}

    @task
    def clean(acquire_a_result: dict):
        clean_df, log = clean_data(acquire_a_result["path"])
        clean_df.to_parquet(CLEAN_OUTPUT_PATH, index=False)
        return {"path": CLEAN_OUTPUT_PATH, "rows": len(clean_df), "rules_triggered": len(log)}

    @task
    def merge(clean_result: dict, acquire_b_result: dict):
        merged_df = merge_data(clean_result["path"], acquire_b_result["path"])
        merged_df.to_parquet(JOINED_OUTPUT_PATH, index=False)
        return {"path": JOINED_OUTPUT_PATH, "rows": len(merged_df)}

    @task
    def store(merge_result: dict):
        build_star_schema(merge_result["path"])
        return "Star schema successfully built and stored."

    @task
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

