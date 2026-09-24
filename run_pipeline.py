import os
from src.common.config import PROCESSED_DATA_PATH
from src.common.logging_setup import setup_logging
from src.ingest.source_a import ingest_source_a
from src.ingest.source_b import ingest_source_b
from src.transform.clean import clean_data
from src.transform.merge import merge_data
from src.validate import rules

logger = setup_logging()

def run_pipeline():
    logger.info("--- STARTING PIPELINE RUN ---")

    try:
        # --- INGEST ---
        logger.info("Ingesting data from Source A (Prices) and Source B (Rainfall)...")
        df_prices = ingest_source_a()
        df_rainfall = ingest_source_b()
        logger.info(f"Ingested Source A: {df_prices.shape[0]} rows, Source B: {df_rainfall.shape[0]} rows.")

        # --- VALIDATE ---
        logger.info("Running validation rules...")
        if df_prices.empty or df_rainfall.empty:
            raise ValueError("Ingestion failed: One or more source dataframes are empty.")
        
        # Log validation stats (non-fatal rule checks)
        bad_prices = rules.rule_positive_price(df_prices)
        logger.info(f"Validation check: Found {len(bad_prices)} negative price rows to clean.")

        # --- TRANSFORM & CLEAN ---
        logger.info("Cleaning Source A data...")
        cleaned_prices, clean_log = clean_data()
        for entry in clean_log:
            logger.info(f"Clean action [{entry['rule']}]: {entry.get('reason', 'N/A')} (Affected: {entry.get('rows_affected', 0)})")

        # --- TRANSFORM & MERGE ---
        logger.info("Merging prices and rainfall data on market and date...")
        final_df = merge_data(cleaned_prices, df_rainfall)
        logger.info(f"Merged dataset shape: {final_df.shape}")

        # --- STORE (Idempotent write) ---
        logger.info("Storing processed dataset (Idempotent overwrite)...")
        os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
        
        # Idempotency mechanism: Overwrite the target file cleanly each run 
        # to ensure re-running never duplicates rows.
        final_df.to_parquet(PROCESSED_DATA_PATH, index=False)
        logger.info(f"Successfully wrote output to {PROCESSED_DATA_PATH}")

        logger.info("---- PIPELINE COMPLETED SUCCESSFULLY ----")

    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    run_pipeline()