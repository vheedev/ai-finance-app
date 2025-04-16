import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
import os

# Save prediction to Excel or CSV
def save_prediction(income, expense, balance):
    now = datetime.now()
    filename = f"prediction_{now.strftime('%Y-%m-%d_%H-%M-%S')}"
    data = pd.DataFrame([{
        "Predicted Income": income,
        "Predicted Expense": expense,
        "Predicted Balance": balance,
        "Date": now.strftime("%Y-%m-%d")
    }])

    try:
        os.makedirs("predictions", exist_ok=True)
        file_path = f"predictions/{filename}.xlsx"
        data.to_excel(file_path, index=False)
        print(f"✅ Prediction saved to {file_path}")
    except Exception as e:
        print("⚠️ Excel failed, saving as CSV instead.")
        file_path = f"predictions/{filename}.csv"
        data.to_csv(file_path, index=False)
        print(f"✅ Prediction saved to {file_path}")

# Visualize prediction with user choice
def plot_prediction(income, expense, balance):
    chart_type = st.radio("Select chart type:", ["Bar Chart", "Line Chart"], horizontal=True)

    months = ["Next Month"]
    income_vals = [income]
    expense_vals = [expense]
    balance_vals = [balance]

    fig, ax = plt.subplots()

    if chart_type == "Bar Chart":
        ax.bar(months, income_vals, label="Income", width=0.2)
        ax.bar(months, expense_vals, label="Expense", width=0.2, bottom=income_vals)
        ax.bar(months, balance_vals, label="Balance", width=0.2)
    else:
        ax.plot(months, income_vals, label="Income", marker="o")
        ax.plot(months, expense_vals, label="Expense", marker="o")
        ax.plot(months, balance_vals, label="Balance", marker="o")

    ax.set_ylabel("Amount")
    ax.set_title("📊 Next Month Financial Prediction")
    ax.legend()
    st.pyplot(fig)

# Example use case
if __name__ == "__main__":
    pred_income = 9250000
    pred_expense = 6500000
    pred_balance = pred_income - pred_expense

    save_prediction(pred_income, pred_expense, pred_balance)
    plot_prediction(pred_income, pred_expense, pred_balance)
