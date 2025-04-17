# File: integrations/gopay.py
import pandas as pd

def fetch_gopay_transactions(username: str) -> pd.DataFrame:
    """
    Fetch Bank gopay transactions for `username` via gopay API.
    Return a DataFrame with columns:
    [ "date", "amount", "description", "type", "account", "username" ].
    """
    # TODO: authenticate to gopay Open API, pull JSON, map into rows:
    data = [
        # { "date": "...", "description": "...", "amount": 1000000,
        #   "type":"Income", "account":"gopay", "username": username },
    ]
    return pd.DataFrame(data)
