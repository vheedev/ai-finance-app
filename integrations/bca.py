cat > integrations/bca.py << 'EOF'

# File: integrations/bca.py
import pandas as pd

def fetch_bca_transactions(username: str) -> pd.DataFrame:
    """
    Stub for Bank BCA integration.
    Return a DataFrame with columns:
      ["date","amount","description","type","account","username"]
    """
    # TODO: authenticate to BCA Open API, pull JSON, map into rows:
    data = [
        # { "date": "...", "description": "...", "amount": 1000000,
        #   "type":"Income", "account":"BCA", "username": username },
    ]
    # TODO: replace with real BCA API calls
    return pd.DataFrame([])

EOF
