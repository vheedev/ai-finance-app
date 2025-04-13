import pandas as pd
import matplotlib.pyplot as plt
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
    while True:
        chart_type = input("View chart as [1] Bar Chart or [2] Line Chart: ").strip()
        if chart_type not in ["1", "2"]:
            print("Please type 1 or 2.")
            continue
        break

    months = ["This Month", "Next Month"]
    income_values = [income * 0.9, income]  # assuming current is 90% of predicted
    expense_values = [expense * 0.95, expense]
    balance_values = [balance * 0.85, balance]

    plt.figure(figsize=(10, 6))

    if chart_type == "1":
        x = range(len(months))
        plt.bar(x, income_values, width=0.2, label="Income")
        plt.bar([i + 0.2 for i in x], expense_values, width=0.2, label="Expense")
        plt.bar([i + 0.4 for i in x], balance_values, width=0.2, label="Balance")
        plt.xticks([i + 0.2 for i in x], months)
        plt.title("Cash Flow Prediction - Bar Chart")

    elif chart_type == "2":
        plt.plot(months, income_values, marker='o', label="Income")
        plt.plot(months, expense_values, marker='o', label="Expense")
        plt.plot(months, balance_values, marker='o', label="Balance")
        plt.title("Cash Flow Prediction - Line Chart")

    plt.ylabel("Amount (Rp)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    os.makedirs("charts", exist_ok=True)
    filename = f"charts/chart_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    plt.savefig(filename)
    print(f"📊 Chart saved to {filename}")
    plt.show()

# Example use case
if __name__ == "__main__":
    pred_income = 9250000
    pred_expense = 6500000
    pred_balance = pred_income - pred_expense

    save_prediction(pred_income, pred_expense, pred_balance)
    plot_prediction(pred_income, pred_expense, pred_balance)
