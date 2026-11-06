import requests

BASE = "http://localhost:8000"

valid = {"market": "Owino", "commodity": "Maize", "date": "2026-03-15", "rainfall_mm": 4.2}
invalid = {"market": "Narnia", "commodity": "Maize", "date": "2026-03-15", "rainfall_mm": -5.0}


def show(title, response):
    print(f"--- {title}: HTTP {response.status_code}")
    print(response.json())


if __name__ == "__main__":
    show("health", requests.get(f"{BASE}/health"))
    
    # call /predict with the valid request
    show("predict (valid)", requests.post(f"{BASE}/predict", json=valid))
    
    # call /predict with an INVALID request (e.g. rainfall_mm = -5)
    show("predict (invalid)", requests.post(f"{BASE}/predict", json=invalid))