import pandas as pd
from src.validate import rules
import hashlib

raw_path = "data/raw/prices.csv"
data_path = "data/processed/prices_clean.parquet"

def hash_file(path):
    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def clean_data(path=raw_path):
    df = pd.read_csv(path)
    log = []

    # duplicate rows
    repeated_rows = rules.rule_duplicate_rows(df)
    if len(repeated_rows) > 0:
        df = df.drop_duplicates(keep="first")
        log.append({
            "rule": "rule_duplicate_rows",
            "action" : "reject",
            "rows_affected" : len(repeated_rows),
            "reason" : "removed exact duplicate rows"
        })

    # duplicate ids
    repeated_ids = rules.rule_duplicate_ids(df)
    if len(repeated_ids) > 0:
        df = df.drop_duplicates(subset=["id"], keep="first")

        log.append({
            "rule" : "rule_duplicate_ids",
            "action" : "reject",
            "rows_affected" : len(repeated_ids),
            "reason" : "removed rows with duplicate ids"
        }) 

    # negative prices
    negative_prices = rules.rule_positive_price(df)
    if len(negative_prices) > 0:
        df = df[df["price"] >= 0]

        log.append({
            "rule" : "rule_positive_price",
            "action" : "reject",
            "rows_affected" : len(negative_prices),
            "reason" : "removed rows with negative prices"
        })

    # invalid dates
    invalid_dates = rules.rule_validate_date(df)
    if len(invalid_dates) > 0:
        df = df.drop(invalid_dates.index)

        log.append({
            "rule" : "rule_validate_date",
            "action" : "reject",
            "rows_affected" : len(invalid_dates),
            "reason" : "removed rows with invalid dates"
        })

    # missing market
    missing_market = rules.rule_missing_market(df)
    if len(missing_market) > 0:
        df["market"] = df["market"].fillna("Unknown")

        log.append({
            "rule" : "rule_missing_market",
            "action" : "impute",
            "rows_affected" : len(missing_market),
            "reason" : "imputed missing markets with unknown"
        })

    # unknown commodity
    unknown_commodities = rules.rule_known_commodity(df)
    if len(unknown_commodities) > 0:
        df = df.drop(unknown_commodities.index)

        log.append({
            "rule": "rule_known_commodity",
            "action": "reject",
            "rows_affected": len(unknown_commodities),
            "reason": "removed unknown commodities"
        })

    # normalize inconsistent commodities
    df["commodity"] = df["commodity"].str.strip().str.title()
    log.append({
        "rule" : "commodity_normalization",
        "action" : "normalize",
        "reason" : "standardized commodity casing"
    })

    return df, log

if __name__ == "__main__":

    before_hash = hash_file(raw_path)

    clean_df, log = clean_data()

    clean_df.to_parquet(data_path, index=False)

    after_hash = hash_file(raw_path)

    print("Raw file Hash before cleaning:", before_hash)
    print("Raw file Hash after cleaning:", after_hash)

    if before_hash == after_hash:
        print(":) Raw file Preserved successfully")
    else:
        print(":( WARNING: Raw file has been modified")

    print(clean_df.head())
    print(log)

