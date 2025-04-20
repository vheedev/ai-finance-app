import pandas as pd
from datetime import datetime, timedelta

def make_dummy_transactions():
    today = datetime.today()
    data = []
    categories = ["Groceries", "Utilities", "Subscription", "Dining", "Transport"]
    desc = ["Supermarket", "Electric Bill", "Netflix", "Cafe", "Taxi"]
    base_date = today - timedelta(days=90)
    for i in range(60):
        date = base_date + timedelta(days=i*1.5)
        cat = categories[i % len(categories)]
        d = desc[i % len(desc)]
        amt = 50000 + (i % 5) * 15000 + (i % 7) * 5000
        data.append({
            "date": date,
            "category": cat,
            "description": d,
            "amount": amt
        })
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df