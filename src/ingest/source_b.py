import requests
import pandas as pd
import os
import time
from src.common.config import (
    SOURCE_B_RAW_PATH,
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
        "rainfall_mm":daily["precipitation_sum"]
    })

    return df

def get_all_market_rain():
    all_market_rain = []

    for market_name, (lat, lon) in MARKET_COORDS.items():
        market_rain = get_market_rainfall(market_name, lat, lon)
        all_market_rain.append(market_rain)
        time.sleep(5)

    return pd.concat(all_market_rain)

def ingest_source_b(path=SOURCE_B_RAW_PATH):
    if os.path.exists(path):
        return pd.read_csv(path)

    df_b = get_all_market_rain()
    df_b.to_csv(path, index=False)
    return df_b