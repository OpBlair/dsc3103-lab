#%%
import pandas as pd

#import rules from /src/validate/rules.py
from src.validate.rules import rule_positive_price, rule_duplicate_ids, rule_duplicate_rows, rule_validate_date, rule_missing_market, rule_known_commodity


#create the dataframe from the prices.csv file(to be used by the rules)
df = pd.read_csv("data/raw/prices.csv")

#call the rules
negative_prices = rule_positive_price(df)

duplicate_ids  = rule_duplicate_ids(df)

duplicate_rows = rule_duplicate_rows(df)

invalid_date = rule_validate_date(df)

missing_market = rule_missing_market(df)

unknown_commodity = rule_known_commodity(df)

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