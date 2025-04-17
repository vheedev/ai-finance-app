# File: integrations/jenius.py
import pandas as pd

def fetch_jenius_transactions(username: str) -> pd.DataFrame:
    """
    Stub for Bank Jenius integration.
    Return a DataFrame with columns:
    [ "date", "amount", "description", "type", "account", "username" ]
    """
    # TODO: authenticate to jenius Open API, pull JSON, map into rows:
    data = [
        # { "date": "...", "description": "...", "amount": 1000000,
        #   "type":"Income", "account":"jenius", "username": username },
    ]
    # TODO: call Jenius API
    return pd.DataFrame(data)
