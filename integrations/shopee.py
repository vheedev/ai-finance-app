# File: integrations/shopee.py
import pandas as pd

def fetch_shopee_transactions(username: str) -> pd.DataFrame:
    """
    Fetch Bank Shopee transactions for `username` via shopee API.
    Return a DataFrame with columns:
    [ "date", "amount", "description", "type", "account", "username" ].
    """
    # TODO: authenticate to shopee Open API, pull JSON, map into rows:
    data = [
        # { "date": "...", "description": "...", "amount": 1000000,
        #   "type":"Income", "account":"shopee", "username": username },
    ]
    return pd.DataFrame(data)
