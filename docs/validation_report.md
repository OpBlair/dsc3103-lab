# Data Validation Report

## 1. Dataset

The raw dataset used for this lab is `data/raw/prices.csv`.
The dataset was generated using `generate_messy_prices.py` and was deliberately created with data quality issues.

## 2. Validation Results

| Rule | Description | Rows Failed | Action |
|---|---|---:|---|
| `rule_positive_price` | Negative prices | 55 | Reject |
| `rule_duplicate_ids` | Duplicate IDs | 16 | Reject |
| `rule_duplicate_rows` | Exact duplicate rows | 11 | Reject |
| `rule_validate_date` | Invalid dates | 15 | Reject |
| `rule_missing_market` | Missing market values | 180 | Impute |
| `rule_known_commodity` | Unknown commodities | 0 | No action |

The validation rules identified duplicate records, duplicate IDs, negative prices, invalid dates, and missing market values. No unknown commodity values were found because all generated commodity values belonged to the accepted categories.

## 3. Category Inconsistencies

The profiler identified multiple representations of the same commodity categories.

| Normalized Category | Original Value | Count |
|---|---|---:|
| beans | BEANS | 268 |
| beans | Beans | 237 |
| maize | MAIZE | 240 |
| maize | Maize | 266 |

These values represent the same commodities but use inconsistent casing. The values were therefore normalized during the cleaning stage.

## 4. Cleaning Decisions

- Negative prices were rejected because prices are expected to be positive.
- Duplicate rows were rejected because they represent repeated records.
- Duplicate IDs were rejected because each record should have a unique identifier.
- Invalid dates were rejected because they cannot be reliably interpreted as valid dates.
- Missing market values were imputed as `Unknown`.
- Unknown commodities were rejected because they are not part of the accepted commodity categories.
- Commodity casing was normalized so that values such as `MAIZE` and `Maize` are represented consistently.

## 5. Raw File Preservation

The SHA-256 hash of `data/raw/prices.csv` was calculated before and after the cleaning process.

**Hash before cleaning:**

`fbc49d599cd5fd962e4845e28a2f970f54a3192e2d2ebb92c8bb68d668f4a80b`

**Hash after cleaning:**

`fbc49d599cd5fd962e4845e28a2f970f54a3192e2d2ebb92c8bb68d668f4a80b`

The hashes were identical, confirming that the raw dataset was not modified during the cleaning process.

## 6. Output

The cleaned dataset was saved as:

`data/processed/prices_clean.parquet`
