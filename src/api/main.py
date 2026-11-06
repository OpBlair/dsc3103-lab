import json

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
import datetime
import pandas as pd

from src.common.features import KNOWN_MARKETS, KNOWN_COMMODITIES, make_features

MODEL_PATH = "models/model.joblib"
META_PATH = "models/model_metadata.json"

app = FastAPI(title="Market Price Prediction Service")

model = joblib.load(MODEL_PATH)
with open(META_PATH) as f:
    metadata = json.load(f)


# (validation) 
class PriceRequest(BaseModel):
    market: Literal[tuple(KNOWN_MARKETS)]
    commodity: Literal[tuple(KNOWN_COMMODITIES)]
    date: datetime.date
    rainfall_mm: float = Field(ge=0.00, le=500.0)


# (health)
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_version": metadata["model_version"],
        "model_type": metadata["model_type"]
    }

# (features)
@app.post("/predict")
def predict(r: PriceRequest):
    # build a one-row DataFrame from the request fields
    df = pd.DataFrame([r.model_dump()])

    # pass it through make_features() from src.common.features,
    X = make_features(df)

    # reorder columns with  X = X[metadata["features"]]
    X = X[metadata["features"]]

    # predict, and return predicted_price (rounded) and model_version.
    pred = model.predict(X)[0]

    return {
        "predicted_price": round(float(pred), 2),
        "model_version": metadata["model_version"],
    }