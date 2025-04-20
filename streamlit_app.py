    else:
        # --------- Top Row: Add New Data button (left) and Download PDF (right) ---------
        col_left, col_right = st.columns([7, 3])
        with col_left:
            if st.button("➕ Add New Data", key="add_new_data_btn"):
                st.session_state.show_add_form = True
        with col_right:
            # Generate summary and PDF for all transactions
            summary_all = show_summary(txns)
            est_tax_all = calculate_tax(txns)
            alerts_all  = check_budget_limits(txns)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Financial Report", ln=1, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 8, f"User: {st.session_state.username}", ln=1)
            pdf.cell(0, 8, f"Period: ALL", ln=1)
            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Summary Statistics", ln=1)
            pdf.set_font("Arial", "", 10)
            for idx, row in summary_all.round(2).iterrows():
                line = ", ".join(f"{col}={row[col]}" for col in summary_all.columns)
                pdf.cell(0, 6, f"{idx}: {line}", ln=1)
            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"Estimated Tax (10%): Rp {est_tax_all:,.2f}", ln=1)
            pdf.ln(3)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Budget Alerts:", ln=1)
            pdf.set_font("Arial", "", 10)
            if not alerts_all:
                pdf.cell(0, 6, "None", ln=1)
            else:
                for cat, amt in alerts_all:
                    pdf.cell(0, 6, f"- {cat}: Rp {amt:,.0f}", ln=1)
            pdf_bytes_all = pdf.output(dest="S").encode("latin-1")
            st.download_button(
                label="⬇️ Download Report",
                data=pdf_bytes_all,
                file_name="financial_report.pdf",
                mime="application/pdf",
                key="download_pdf_homepage"
            )

        # --- Show Add Form or Main Dashboard ---
        if st.session_state.get("show_add_form", False):
            st.markdown("## 📝 Add New Transaction")
            with st.form("add_txn_form", clear_on_submit=True):
                t_date = st.date_input("Date", value=date.today())
                t_cat  = st.text_input("Category")
                t_amt  = st.number_input("Amount", min_value=0.0, step=0.01)
                t_desc = st.text_input("Description")
                submit = st.form_submit_button("Add Transaction")
                if submit:
                    add_transaction(
                        st.session_state.username,
                        t_date,
                        t_cat,
                        t_amt,
                        t_desc,
                    )
                    st.success("Transaction added!")
                    st.session_state.show_add_form = False
                    st.rerun()
            if st.button("⬅️ Back to Dashboard", key="back_to_dashboard_btn"):
                st.session_state.show_add_form = False
                st.rerun()
        else:
            tab1, tab2 = st.tabs(["Quick Select", "Calendar View"])

            # --- Quick Select ---
            with tab1:
                sel_period = st.selectbox(
                    "Pick one of the last 3 months",
                    last_months,
                    index=last_months.index(st.session_state.get('sel_period_quick', last_months[-1])),
                    key="sel_period_quick"
                )
                year, month = map(int, sel_period.split("-"))
                filt1 = txns[
                    (txns["date"].dt.year  == year) &
                    (txns["date"].dt.month == month)
                ]
                st.write("🔍 Filtered rows (Quick-Select):", filt1.shape[0])

                summary1 = show_summary(filt1)
                est_tax1 = calculate_tax(filt1)
                alerts1  = check_budget_limits(filt1)

                st.markdown("### 📊 Summary Report")
                summary1_df = summary1.reset_index()
                if len(summary1_df.columns) == 2:
                    summary1_df.columns = ["Category", "Total Amount"]
                st.bar_chart(summary1_df.set_index(summary1_df.columns[0])[summary1_df.columns[1]])
                st.dataframe(summary1_df, use_container_width=True)

                st.markdown("### 💡 Estimated Tax")
                st.info(f"Rp {est_tax1:,.2f}")

                st.markdown("### 🚦 Budget Alerts")
                if not alerts1:
                    st.write("No alerts 🎉")
                else:
                    for cat, amt in alerts1:
                        st.write(f"- {cat}: Rp {amt:,.0f}")

            # --- Calendar View ---
            with tab2:
                _, btn_col = st.columns([7, 3])
                download_slot = btn_col.empty()

                start_date, end_date = st.date_input(
                    "🗓 Select report range",
                    value=(today.replace(day=1), today),
                    format="YYYY-MM-DD"
                )
                mask = (
                    (txns["date"] >= pd.to_datetime(start_date)) &
                    (txns["date"] <= pd.to_datetime(end_date))
                )
                filtered = txns.loc[mask]
                st.write("🔍 Filtered rows (Calendar-View):", filtered.shape[0])

                summary = show_summary(filtered)
                est_tax = calculate_tax(filtered)
                alerts  = check_budget_limits(filtered)

                st.markdown("### 📊 Summary Report")
                summary_df = summary.reset_index()
                if len(summary_df.columns) == 2:
                    summary_df.columns = ["Category", "Total Amount"]
                st.bar_chart(summary_df.set_index(summary_df.columns[0])[summary_df.columns[1]])
                st.dataframe(summary_df, use_container_width=True)

                st.markdown("### 💡 Estimated Tax")
                st.info(f"Rp {est_tax:,.2f}")

                st.markdown("### 🚦 Budget Alerts")
                if not alerts:
                    st.write("No alerts 🎉")
                else:
                    for cat, amt in alerts:
                        st.write(f"- {cat}: Rp {amt:,.0f}")