# File: integrations/tokopedia.py
import pandas as pd

def fetch_tokopedia_transactions(username: str) -> pd.DataFrame:
    """
    Fetch Tokopedia transactions for `username` via Tokopedia API.
    Return a DataFrame with columns:
    [ "date", "amount", "description", "type", "account", "username" ].
    """
    # TODO: authenticate to Tokopedia Open API, pull JSON, map into rows:
    data = [
        # { "date": "...", "description": "...", "amount": 1000000,
        #   "type":"Income", "account":"Tokopedia", "username": username },
    ]
    return pd.DataFrame(data)
