import requests
import pandas as pd
from src.common.config import (
    SOURCE_A_RAW_PATH,
    MARKET_COORDS,
    RAINFALL_START_DATE,
    RAINFALL_END_DATE,
    RAINFALL_URL
)

def get_market_rainfall(market_name, latitude, longitude, start_date=RAINFALL_START_DATE, end_date=RAINFALL_END_DATE):

    params = {
        "latitude":latitude,
        "longitude":longitude,
        "start_date":start_date,
        "end_date":end_date,
        "timezone":"auto",
        "daily":"precipitation_sum"
    }

    response=requests.get(RAINFALL_URL,params=params,timeout=10)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to get data for {market_name} : Status {response.status_code}")

    daily = response.json()["daily"]

    df = pd.DataFrame({
        "date":daily["time"],
        "market":market_name,
        "rainfall":daily["precipitation_sum"]
    })

    return df

def ingest_source_b():
    all_dfs = []

    for market_name, (lat, lon) in MARKET_COORDS.items():
        try:
            market_df = get_market_rainfall(market_name, lat, lon)
            all_dfs.append(market_df)
        except Exception as e:
            print(f"Skipping {market_name} due an error {e}")

    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return pd.DataFrame()