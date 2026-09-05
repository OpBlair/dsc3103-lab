"""
 `#%%` runs the code like a notebook.
"""

#%%
import csv
import random
from datetime import datetime, timedelta

#%%
random.seed(42)

rows = []
base_date = datetime(2020, 1, 1)
markets = ["Mukono", "Bwaise", "Nakasero", "Kansanga", None]
commodities = ["Maize", "MAIZE", "Beans", "BEANS"]


# Fake Data => {id, date, market, commodity, price}
for i in range(1000):
    row = {
        "id" : i if random.random() > 0.02 else i - 1,
        "date" :  (base_date + timedelta(days=random.randint(0, 1000))).strftime("%Y-%m-%d") if random.random() > 0.02 else "2020-14-50",
        "market" : random.choice(markets),
        "commodity" : random.choice(commodities),
        "price" : random.randint(500, 5000) if random.random() > 0.05 else -2000
    }

    rows.append(row)

with open("data/raw/prices.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=("id","date","market","commodity","price"))
    writer.writeheader()
    writer.writerows(rows)