#%%
import pandas as pd

# import rules from /src/validate/rules.py
from src.validate.rules import rule_positive_price, rule_duplicate_ids, rule_duplicate_rows, rule_validate_date, rule_missing_market, rule_known_commodity, rule_negative_rain

# import source_a from /src/ingest
from src.ingest.source_a import ingest_source_a

# import source_b from src/ingest
from src.ingest.source_b import ingest_source_b

# import config for market coordinates
from src.common.config import MARKET_COORDS

# import from transform
from src.transform.clean import clean_data
from src.transform.merge import merge_data

#create the dataframe from the prices.csv file(to be used by the rules)
df = pd.read_csv("data/raw/prices.csv")


# check negative prices
print("------ Negative Prices ------")
negative_prices = rule_positive_price(df)
print(negative_prices)
print("-"*70)

# check duplicate IDs
print("------ Duplicate IDs -------")
duplicate_ids  = rule_duplicate_ids(df)
print(duplicate_ids)
print("-"*70)

# check duplicate rows
print("------ Duplicate Rows ------")
duplicate_rows = rule_duplicate_rows(df)
print(duplicate_rows)
print("-"*70)

# check invalid dates
print("------ Invalid Date -------")
invalid_date = rule_validate_date(df)
print(invalid_date)
print("-"*70)

# check missing market
print("------ Missing Market -------")
missing_market = rule_missing_market(df)
print(missing_market)
print("-"*70)

# check unknown commodity
print("------ Unknown Commodity ----")
unknown_commodity = rule_known_commodity(df)
print(unknown_commodity)
print("-"*70)

# check for source A data
print("------ Source A Verification -----")
source_a_df = ingest_source_a()
print(f"{'-'*5} prices_shape {'-'*5}")
print(source_a_df.shape)
print("-"*70)

# check source B data
source_b_df = ingest_source_b()
print("------rainfall_shape-----")
print(source_b_df.shape)
print(source_b_df.head(10))
print("-"*70)

# check cleaned source_a data
clean_prices, _ = clean_data()
print("length of clean prices data")
print(len(clean_prices))
print("-"*70)

# check for negative rainfall data
negative_rain = rule_negative_rain(source_b_df)
print("Negative rain Datat")
print(negative_rain)
print("-"*70)

# check for invalid dates in source_b data
bad_dates = rule_validate_date(source_b_df)
print("Number of invalid dates in source_b data")
print(len(bad_dates))
print("-"*70)

# Merge and Confirm that the data merged successfully
merged_data = merge_data(clean_prices, source_b_df)
print(f"Length of Merged data = {len(merged_data)}")
print(merged_data.head(10))
print("-"*70)