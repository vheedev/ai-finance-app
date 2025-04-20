import streamlit as st
import pandas as pd
from fpdf import FPDF

# Inject custom CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div style='background: #e8f0fe; border-radius: 10px; padding: 20px; margin-bottom:16px;'>
    <h2 style='color:#1a237e'>AI Finance Dashboard</h2>
    <p>Welcome, <b>{}</b>! Your personalized overview.</p>
</div>
""".format(st.session_state.get("username","Guest")), unsafe_allow_html=True)

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