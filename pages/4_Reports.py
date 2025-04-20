import streamlit as st
import pandas as pd
from fpdf import FPDF

st.title("📄 Reports & Export")

# Example dummy report button
if st.button("Download Financial Report as PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Financial Report", ln=1, align="C")
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name="financial_report.pdf",
        mime="application/pdf"
    )

st.subheader("Export Transactions")
# ... add export as CSV, Excel, etc.