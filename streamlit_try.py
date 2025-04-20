import streamlit as st
import pandas as pd

data = pd.DataFrame({
    "Category": ["Food", "Rent", "Fun"],
    "Total Amount": [100, 1200, 300]
})
st.markdown("### 📊 Summary Report")
st.bar_chart(data.set_index("Category")["Total Amount"])
st.dataframe(data)