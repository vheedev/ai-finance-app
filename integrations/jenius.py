# File: integrations/jenius.py
import pandas as pd

def fetch_jenius_transactions(username: str) -> pd.DataFrame:
    """
    Fetch Bank jenius transactions for `username` via jenius API.
    Return a DataFrame with columns:
    [ "date", "amount", "description", "type", "account", "username" ].
    """
    # TODO: authenticate to jenius Open API, pull JSON, map into rows:
    data = [
        # { "date": "...", "description": "...", "amount": 1000000,
        #   "type":"Income", "account":"jenius", "username": username },
    ]
    return pd.DataFrame(data)
