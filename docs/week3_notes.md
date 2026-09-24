# Week 3 Notes — DSC3103

## Step 3: ETL OR ELT Justification
**Choice:** We utilized a **Hybrid ELT and ETL** approach tailored to our two sources:
1. **Source A (`prices.csv` — ELT Approach):** Landed directly into our storage tier first to preserve the raw audit trail, with cleaning and transformation happening downstream.
2. **Source B (`rainfall.csv` via Open-Meteo API — ETL Approach):** Reshaped and extracted from the JSON payload into a tabular structure *before* persistence.
3. **Integration:** Both sources are merged on a composite key (`market` and `date`) during the transformation stage.

**Justification:** 
1. **Data Quality & Cleaning Needs:** Our primary data sources (Market `prices.csv` and Open-Meteo `rainfall.csv`) contain messy, unvalidated data types, missing values, and formatting inconsistencies (e.g., negative prices, malformed dates). Cleaning and validating these rows *before* loading them into our storage layer prevents dirty data from polluting downstream analytical queries.
2. **Target Store Simplicity:** Our target store is a structured local file/database layer. Transforming the data in-memory via Pandas allows us to enforce strict schemas, handle type casting, and drop or quarantine invalid records cleanly during the pipeline run.
3. **Volume vs. Complexity:** Because our dataset size is moderate (local CSV/API scale), the performance overhead of transforming in-memory before loading is negligible compared to the massive benefit of clean, predictable table schemas.

---

## Step 8: Idempotency Mechanism
**Choice:** We implemented **Overwrite via Composite Key Merging**.
**Justification:** Running `run_pipeline.py` multiple times consecutively on the same input files will not duplicate rows in the final processed output (`data/processed/final_merged.parquet`). The pipeline safely overwrites the target file each run, ensuring a clean, reproducible state without inflating row counts or corrupting metrics.

## Step 9: Automated Testing & Configuration
**Tool:** `pytest`
**Execution Note:** Because our project uses a `src/` layout structure, running `pytest` directly can sometimes trigger a `ModuleNotFoundError` if Python doesn't know where the root package lives. 
* To resolve this during local development, we run tests using:
  ```bash
  PYTHONPATH=. pytest

* Also moved ```run_pipeline.py``` from ```src``` directory to ```parent_directory```.

---
