# File: integrations/moka.py
import pandas as pd

def fetch_moka_transactions(username: str) -> pd.DataFrame:
    """
    Stub for Bank moka integration.
    Return a DataFrame with columns:
      ["date","amount","description","type","account","username"]
    """
    # TODO: authenticate to moka Open API, pull JSON, map into rows:
    data = [
        # { "date": "...", "description": "...", "amount": 1000000,
        #   "type":"Income", "account":"moka", "username": username },
    ]
    # TODO: replace with real moka API calls
    return pd.DataFrame([])
