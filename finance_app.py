import os
import hashlib
import pandas as pd
from datetime import datetime

USERS_DB = "users.csv"

# --- User Authentication ---

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if not os.path.exists(USERS_DB):
        df = pd.DataFrame(columns=["username", "password"])
    else:
        df = pd.read_csv(USERS_DB)

    if username in df["username"].values:
        return False, "Username already exists."

    hashed = hash_password(password)
    new_user = pd.DataFrame([{"username": username, "password": hashed}])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USERS_DB, index=False)
    return True, "Registration successful."

def login_user(username, password):
    if not os.path.exists(USERS_DB):
        return False, "No registered users found."

    df = pd.read_csv(USERS_DB)
    hashed = hash_password(password)

    if ((df["username"] == username) & (df["password"] == hashed)).any():
        return True, "Login successful."
    return False, "Incorrect username or password."

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

def show_summary(transactions):
    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["date"])
    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()
    balance = income + expense

    print("\n==== Financial Summary ====")
    print(f"Total Income : Rp {income:,.0f}")
    print(f"Total Expense: Rp {abs(expense):,.0f}")
    print(f"Balance      : Rp {balance:,.0f}")
    print("\n==== Transactions ====")
    print(df[["date", "description", "amount", "account"]])
    print("=========================\n")

# --- Main App ---

def main():
    print("=== Welcome to Financial AI Automation App ===")
    while True:
        choice = input("Login [1] | Register [2] | Exit [0]: ").strip()
        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            success, msg = login_user(username, password)
            print(msg)
            if success:
                transactions = fetch_all_transactions()
                show_summary(transactions)
        elif choice == "2":
            username = input("Choose Username: ")
            password = input("Choose Password: ")
            success, msg = register_user(username, password)
            print(msg)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please type 1, 2, or 0.")

# --- Entry Point ---
if __name__ == "__main__":
    main()
