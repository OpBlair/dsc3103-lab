#%%
import pandas as pd

# import rules from /src/validate/rules.py
from src.validate.rules import rule_positive_price, rule_duplicate_ids, rule_duplicate_rows, rule_validate_date, rule_missing_market, rule_known_commodity

# import source_a from /src/ingest
from src.ingest.source_a import ingest_source_a

# import source_b from src/ingest
from src.ingest.source_b import ingest_source_b

# import config for market coordinates
from src.common.config import MARKET_COORDS

#create the dataframe from the prices.csv file(to be used by the rules)
df = pd.read_csv("data/raw/prices.csv")

#call the rules
negative_prices = rule_positive_price(df)

duplicate_ids  = rule_duplicate_ids(df)

duplicate_rows = rule_duplicate_rows(df)

invalid_date = rule_validate_date(df)

missing_market = rule_missing_market(df)

unknown_commodity = rule_known_commodity(df)

source_a_df = ingest_source_a()

#print the results
print("------ Negative Prices ------")
print(negative_prices)

print("------ Duplicate IDs -------")
print(duplicate_ids)

print("------ Duplicate Rows ------")
print(duplicate_rows)

print("------ Invalid Date -------")
print(invalid_date)

print("------ Missing Market -------")
print(missing_market)

print("------ Unknown Commodity ----")
print(unknown_commodity)

print("------ Source A Verification -----")
print(source_a_df.shape)

print("------ Testing API Response on market coordinates -----")

try:
    source_b_df = ingest_source_b()

    print("Success! the DataFrame has returned succcessfully")
    print(f"\nSource B data First few rows: \n{source_b_df.head()}")
    print(f"\nSource B data shape: {source_b_df.shape}")
    print(f"\nRecord count {source_b_df["market"].value_counts()}")
except Exception as e:
    print(f"Source API ingestion on Mukono coordinates failed: {e}")