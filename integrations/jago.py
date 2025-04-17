# File: integrations/jago.py
import pandas as pd

def fetch_jago_transactions(username: str) -> pd.DataFrame:
    """
    Fetch Bank jago transactions for `username` via jago API.
    Return a DataFrame with columns:
    [ "date", "amount", "description", "type", "account", "username" ].
    """
    # TODO: authenticate to jago Open API, pull JSON, map into rows:
    data = [
        # { "date": "...", "description": "...", "amount": 1000000,
        #   "type":"Income", "account":"jago", "username": username },
    ]
    return pd.DataFrame(data)
