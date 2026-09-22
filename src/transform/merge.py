def merge_data(clean_df, rainfall_df):
    merged = clean_df.merge(rainfall_df, on=["market", "date"], how="inner")

    return merged