from fpdf import FPDF
from datetime import datetime
import os

def generate_pdf_report(username, income, expense, balance, tax, file_path="reports"):
    os.makedirs(file_path, exist_ok=True)
    now = datetime.now()
    filename = f"{file_path}/report_{username}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Financial Summary Report", ln=1, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"User: {username}", ln=2)
    pdf.cell(200, 10, txt=f"Date: {now.strftime('%d %B %Y %H:%M')}", ln=3)
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Summary:", ln=4)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Predicted Income     : Rp {income:,.0f}", ln=5)
    pdf.cell(200, 10, txt=f"Predicted Expense    : Rp {expense:,.0f}", ln=6)
    pdf.cell(200, 10, txt=f"Predicted Balance    : Rp {balance:,.0f}", ln=7)
    pdf.cell(200, 10, txt=f"Estimated Tax (10%)  : Rp {tax:,.0f}", ln=8)

    pdf.output(filename)
    print(f"📄 PDF report exported to {filename}")

# Example test
if __name__ == "__main__":
    generate_pdf_report("vheecious", 9250000, 6500000, 2750000, 1100000)
