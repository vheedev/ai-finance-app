import pandas as pd
from datetime import datetime

# --- Simulated Financial Data (for banks, POS, ecommerce) ---

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

# --- Summary Display ---

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
    monthly_income = df[
        (df["type"] == "income") & 
        (df["month"] == current_month) & 
        (df["year"] == current_year)
    ]["amount"].sum()
    return monthly_income * (tax_rate_percent / 100)
