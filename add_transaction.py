import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression

# --- Simulated Financial Data ---

def fetch_all_transactions():
    return [
        {"date": "2025-04-01", "description": "Gaji Bulanan", "amount": 7000000, "type": "income", "account": "BCA"},
        {"date": "2025-04-02", "description": "Belanja Tokopedia via GoPay", "amount": -1500000, "type": "expense", "account": "GoPay"},
        {"date": "2025-04-03", "description": "Investasi Mandiri", "amount": -3000000, "type": "expense", "account": "Mandiri"},
        {"date": "2025-04-04", "description": "Modal Dagang Shopee", "amount": -2000000, "type": "expense", "account": "ShopeePay"},
        {"date": "2025-04-05", "description": "Penjualan via Moka POS", "amount": 2500000, "type": "income", "account": "Moka POS"},
        {"date": "2025-04-08", "description": "Penjualan Tokopedia", "amount": 1500000, "type": "income", "account": "Tokopedia"},
        {"date": "2025-04-09", "description": "Beli bahan baku Tokopedia", "amount": -500000, "type": "expense", "account": "Tokopedia"},
        {"date": "2025-04-10", "description": "Bayar Listrik PLN", "amount": -500000, "type": "expense", "account": "BCA"},
        {"date": "2025-04-12", "description": "Makan Siang", "amount": -100000, "type": "expense", "account": "GoPay"},
    ]

# --- Summary ---

def show_summary(transactions):
    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"])
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    balance = income + expense
    return income, expense, balance, df

# --- Tax Calculation ---

def calculate_tax(transactions, tax_rate_percent=10):
    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    current_month = datetime.today().month
    current_year = datetime.today().year
    monthly_income = df[(df["type"] == "income") & (df["month"] == current_month) & (df["year"] == current_year)]["amount"].sum()
    return monthly_income * (tax_rate_percent / 100)

# --- Budget Overspending Check ---

def check_budget_limits(transactions, personal_limit=2000000, business_limit=4000000):
    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    current_month = datetime.today().month
    current_year = datetime.today().year
    df = df[(df["month"] == current_month) & (df["year"] == current_year)]

    def categorize(desc):
        desc = desc.lower()
        if "makan" in desc or "belanja" in desc:
            return "personal"
        elif "modal" in desc or "tokopedia" in desc or "bahan" in desc:
            return "business"
        else:
            return "other"

    df["category"] = df["description"].apply(categorize)
    personal_total = df[df["category"] == "personal"]["amount"].sum()
    business_total = df[df["category"] == "business"]["amount"].sum()

    alerts = []
    if abs(personal_total) > personal_limit:
        alerts.append(f"⚠️ Pengeluaran pribadi bulan ini melebihi batas Rp {personal_limit:,.0f}")
    if abs(business_total) > business_limit:
        alerts.append(f"⚠️ Pengeluaran bisnis bulan ini melebihi batas Rp {business_limit:,.0f}")
    return alerts

# --- AI Prediction of Next Month Cash Flow ---

def predict_next_month(transactions):
    df_summary = pd.DataFrame(transactions)
    df_summary["month"] = pd.to_datetime(df_summary["date"]).dt.month
    df_summary["year"] = pd.to_datetime(df_summary["date"]).dt.year
    df_income = df_summary[df_summary["type"] == "income"].groupby("month")["amount"].sum().reset_index()
    df_expense = df_summary[df_summary["type"] == "expense"].groupby("month")["amount"].sum().abs().reset_index()
    df_model = pd.merge(df_income, df_expense, on="month", how="outer", suffixes=("_income", "_expense")).fillna(0)
    current_month = datetime.today().month
    X = df_model[["month"]]
    y_income = df_model["amount_income"]
    y_expense = df_model["amount_expense"]
    model_income = LinearRegression().fit(X, y_income)
    model_expense = LinearRegression().fit(X, y_expense)
    next_month = pd.DataFrame([[current_month + 1]], columns=["month"])
    predicted_income = model_income.predict(next_month)[0]
    predicted_expense = model_expense.predict(next_month)[0]
    predicted_balance = predicted_income - predicted_expense
    return predicted_income, predicted_expense, predicted_balance
