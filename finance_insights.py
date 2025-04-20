import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_next_month_expense(df):
    df = df.copy()
    if 'date' not in df:
        return None, "No date column found."
    df['year_month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('year_month')['amount'].sum().reset_index()
    if len(monthly) < 2:
        return None, "Not enough data for forecast."
    X = np.arange(len(monthly)).reshape(-1, 1)
    y = monthly['amount'].values
    model = LinearRegression().fit(X, y)
    next_idx = np.array([[len(monthly)]])
    forecast = model.predict(next_idx)[0]
    return forecast, f"Based on a linear trend from {len(monthly)} months of data."

def suggest_budget(df):
    df = df.copy()
    if 'date' not in df:
        return None, "No date column found."
    df['year_month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('year_month')['amount'].sum()
    if len(monthly) == 0:
        return None, "No spending data available."
    avg = monthly.mean()
    return avg, f"Based on the average of the last {len(monthly)} months."

def detect_recurring(df):
    df = df.copy()
    if 'date' not in df:
        return None
    df['year_month'] = df['date'].dt.to_period('M')
    key_cols = ['category', 'description', 'amount']
    for col in key_cols:
        if col not in df:
            return None
    recurring = (
        df.groupby(key_cols)['year_month']
        .nunique()
        .reset_index()
        .rename(columns={'year_month': 'recurs_months'})
    )
    recurring = recurring[recurring['recurs_months'] >= 2]
    return recurring