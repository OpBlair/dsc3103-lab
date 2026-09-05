import pandas as pd
import matplotlib.pyplot as plt
from src.validate import rules 

raw_path = "data/raw/prices.csv"

# inferred schema(column names and data types)
def inferred_schema(df):
    print("\n ----- Infered Schema -----")
    print(df.dtypes)

# row count
def row_count(df):
    print("\n ------ Row count ------")
    print(len(df))

# missing values per column
def missing_values(df):
    print("\n ----- Missing Count -----")
    print(df.isnull().sum())

# duplicate counts 
def duplicate_id(df):
    duplicate_ids = rules.rule_duplicate_ids(df)
    print("\n ----- Duplicate Ids ------")
    print(len(duplicate_ids))
    
def duplicate_row(df):
    duplicate_rows = rules.rule_duplicate_rows(df)
    print("\n ----- Duplicate Rows ------")
    print(len(duplicate_rows))

# Invalid values(negative values)
def negative_values(df):
    negative_values = rules.rule_positive_price(df)
    print("\n ----- Negative Prices -----")
    print(len(negative_values))

# Invalid values(negative values)
def invalid_dates(df):
    invalid_dates = rules.rule_validate_date(df)
    print("\n ----- Invalid Dates -----")
    print(len(invalid_dates))

# Inconsistent Categories
def inconsistent_categories(df):
    print("\n ----- Inconsistent Categories -----")
    normalised = df["commodity"].str.strip().str.lower()
    profile = df.assign(normalised_commodity=normalised).groupby(["normalised_commodity", "commodity"]).size()
    print(profile)

# summary statistics
def summary_statistics(df):
    print("\n ----- Summary Statistics ----")
    print(df.describe())

# histogram plot
def plot_price_histogram(df):
    plt.hist(df["price"], bins=20, edgecolor="black")
    plt.title("Distribution of Prices")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.show()
    
def run_files(path=raw_path):
    df = pd.read_csv(path)
    inferred_schema(df)
    row_count(df)
    negative_values(df)
    missing_values(df)
    duplicate_id(df)
    duplicate_row(df)
    invalid_dates(df)
    inconsistent_categories(df)
    summary_statistics(df)
    plot_price_histogram(df)

if __name__ == "__main__":
    run_files()