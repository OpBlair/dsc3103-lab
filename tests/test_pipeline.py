import pandas as pd
from src.validate.rules import rule_positive_price

def test_rule_positive_price():

    mock_data = pd.DataFrame({
        "id": [1,2,3],
        "price": [1500, -200, 3000]
    })

    bad_rows = rule_positive_price(mock_data)

    assert len(bad_rows) == 1
    assert bad_rows.iloc[0]["price"] == -200
    print("Test finished successfully")