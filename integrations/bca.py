# File: integrations/bca.py
import pandas as pd

def fetch_bca_transactions(username: str) -> pd.DataFrame:
    """
    Fetch Bank BCA transactions for `username` via BCA API.
    Return a DataFrame with columns:
    [ "date", "amount", "description", "type", "account", "username" ].
    """
    # TODO: authenticate to BCA Open API, pull JSON, map into rows:
    data = [
        # { "date": "...", "description": "...", "amount": 1000000,
        #   "type":"Income", "account":"BCA", "username": username },
    ]
    return pd.DataFrame(data)
