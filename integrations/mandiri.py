# File: integrations/mandiri.py
import pandas as pd

def fetch_mandiri_transactions(username: str) -> pd.DataFrame:
    """
    Fetch Bank mandiri transactions for `username` via mandiri API.
    Return a DataFrame with columns:
    [ "date", "amount", "description", "type", "account", "username" ].
    """
    # TODO: authenticate to mandiri Open API, pull JSON, map into rows:
    data = [
        # { "date": "...", "description": "...", "amount": 1000000,
        #   "type":"Income", "account":"mandiri", "username": username },
    ]
    return pd.DataFrame(data)
