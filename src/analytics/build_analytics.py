import os
import time
import pandas as pd
import duckdb as db
from src.common.config import RAW_JOINED_PATH, DB_PATH

def baseline_query():
    t0 = time.perf_counter()
    result = db.sql(f"""
        SELECT commodity, market, AVG(price) AS mean_price
        FROM '{RAW_JOINED_PATH}'
        WHERE commodity in ('Maize', 'Beans')
        GROUP BY commodity, market
        ORDER BY commodity, mean_price DESC
    """).df()

    elapsed = time.perf_counter() - t0

    print("==== Step 1: Baseline query (flat Parquet) ====")
    print(result)
    print(f"Time: {elapsed:.4f}s | File size: {os.path.getsize(RAW_JOINED_PATH)} bytes")

    return elapsed, result

def build_star_schema():
    df = pd.read_parquet(RAW_JOINED_PATH)
    duckdb_conn = db.connect(DB_PATH)

    # Market dimension table
    dim_market = df[["market"]].drop_duplicates().reset_index(drop=True)
    dim_market["market_id"] = dim_market.index
    duckdb_conn.execute("CREATE OR REPLACE TABLE dim_market AS SELECT * FROM dim_market")

    # Commodity dimension table
    dim_commodity = df[["commodity"]].drop_duplicates().reset_index(drop=True)
    dim_commodity["commodity_id"] = dim_commodity.index
    duckdb_conn.execute("CREATE OR REPLACE TABLE dim_commodity AS SELECT * FROM dim_commodity")

    # Fact table
    fact_df = df.merge(dim_market, on="market").merge(dim_commodity, on="commodity")
    fact_df = fact_df[["id", "date", "market_id", "commodity_id", "price", "rainfall_mm"]]
    duckdb_conn.execute("CREATE OR REPLACE TABLE fact_price_observation AS SELECT * FROM fact_df")

    print(f"\n==== Step 3: Star Schema Built ====")
    print(f"Fact Table row count: {duckdb_conn.sql("SELECT COUNT(*) FROM fact_price_observation").fetchone()[0]}")
    duckdb_conn.close()

def run_analytical_queries():
    duckdb_conn = db.connect(DB_PATH)

    print(f"\n==== Query 1: Average price by market ====")
    print(duckdb_conn.sql("""
        SELECT dm.market, AVG(f.price) AS mean_price
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        GROUP BY dm.market
        ORDER BY mean_price DESC
    """).df())

    print(f"\n==== Query 2: Observation count by commodity ====")
    print(duckdb_conn.sql("""
        SELECT dc.commodity, COUNT(*) AS n_observations
        FROM fact_price_observation f
        JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
        GROUP BY dc.commodity
        ORDER BY n_observations DESC
    """).df())

    # Average price and rainfall by commodity
    print(f"\n=== Query 3: Average price and rainfall by commodity ===")
    print(duckdb_conn.sql("""
        SELECT dc.commodity, AVG(f.price) AS mean_price, AVG(f.rainfall_mm) AS mean_rainfall
        FROM fact_price_observation f
        JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
        GROUP BY dc.commodity
        ORDER BY mean_price DESC
    """).df())

    # Maximum price recorded per market
    print(f"\n=== Query 4: Maximum price by market ===")
    print(duckdb_conn.sql("""
        SELECT dm.market, MAX(f.price) AS max_price
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        GROUP BY dm.market
        ORDER BY max_price DESC
    """).df())

    # Observation count breakdown by market and commodity
    print(f"\n=== Query 5: Observation count by market and commodity ===")
    print(duckdb_conn.sql("""
        SELECT dm.market, dc.commodity, COUNT(*) AS observations
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
        GROUP BY dm.market, dc.commodity
        ORDER BY observations DESC
    """).df())

    duckdb_conn.close()

def compare_performance():
    t0 = time.perf_counter()

    db.sql(f"""
        SELECT market, AVG(price) FROM '{RAW_JOINED_PATH}' GROUP BY market
    """).df()

    flat_time = time.perf_counter() - t0

    # Star Schema Timing
    t1 = time.perf_counter()
    duckdb_conn = db.connect(DB_PATH)
    duckdb_conn.sql("""
        SELECT dm.market, AVG(f.price)
        FROM fact_price_observation f
        JOIN dim_market dm on f.market_id = dm.market_id
        GROUP BY dm.market
    """).df()
    duckdb_conn.close()

    star_time = time.perf_counter() - t1

    print(f"\n==== Step 5: Performance Comparison ====")
    print(f"Flat Parquet query time: {flat_time:.4f}s")
    print(f"Star schema query time: {star_time:.4f}s")

if __name__ == "__main__":
    elapsed, result = baseline_query()

    print(f"\n==== Markets with the Highest Mean for Each Commodity ====\n")
    for commodity in ['Maize', 'Beans']:
        commodity_data = result[result['commodity'] == commodity]
        highest = commodity_data.loc[commodity_data['mean_price'].idxmax()]

        print(f"{commodity}: {highest['market']} "
            f"has the highest mean price of {highest['mean_price']:.2f}"
        )

    build_star_schema()
    run_analytical_queries()
    compare_performance()
