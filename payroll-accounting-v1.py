import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="Payroll Accounting", layout="wide")

# Title and Introduction
st.title("Payroll Accounting")
st.write("""
Payroll accounting involves calculating employee wages, withholdings (taxes, benefits), and employer obligations (e.g., payroll taxes), then recording these in the accounting system. Key aspects include:
- Gross pay calculation (hourly, salaried).
- Deductions (federal/state taxes, insurance).
- Net pay distribution.
- Journal entries for expenses and liabilities.
""")
st.write("This app simulates payroll processing and its accounting impact.")

# Initialize Session State
if "employees" not in st.session_state:
    st.session_state.employees = []
if "payroll_records" not in st.session_state:
    st.session_state.payroll_records = []

# Sidebar Navigation
st.sidebar.title("Payroll Tools")
option = st.sidebar.selectbox(
    "Choose a Task",
    ["Manage Employees", "Process Payroll", "Payroll Ledger", "Financial Impact", "Reports & Visualization"]
)
pay_period_start = st.sidebar.date_input("Pay Period Start", value=datetime(2025, 3, 1))
pay_period_end = st.sidebar.date_input("Pay Period End", value=datetime(2025, 3, 15))

# --- Manage Employees ---
if option == "Manage Employees":
    st.subheader("Manage Employees")
    st.write("Add or edit employee details for payroll processing.")

    with st.form(key="employee_form"):
        employee_id = st.text_input("Employee ID", "e.g., EMP001")
        name = st.text_input("Employee Name")
        pay_type = st.selectbox("Pay Type", ["Hourly", "Salary"])
        rate = st.number_input(f"{'Hourly Rate' if pay_type == 'Hourly' else 'Annual Salary'} ($)", min_value=0.0, value=15.0 if pay_type == "Hourly" else 40000.0)
        hours_per_period = st.number_input("Hours per Pay Period (Hourly Only)", min_value=0.0, value=80.0, disabled=pay_type == "Salary")
        submit_button = st.form_submit_button(label="Add/Update Employee")

    if submit_button:
        if not employee_id or not name:
            st.error("Employee ID and Name are required!")
        else:
            employee = {
                "Employee ID": employee_id,
                "Name": name,
                "Pay Type": pay_type,
                "Rate": rate,
                "Hours per Period": hours_per_period if pay_type == "Hourly" else 0
            }
            # Update if exists, else add
            existing = [e for e in st.session_state.employees if e["Employee ID"] == employee_id]
            if existing:
                st.session_state.employees = [e if e["Employee ID"] != employee_id else employee for e in st.session_state.employees]
                st.success(f"Updated employee: {name}")
            else:
                st.session_state.employees.append(employee)
                st.success(f"Added employee: {name}")

    # Display Employees
    if st.session_state.employees:
        st.write("### Employee List")
        employees_df = pd.DataFrame(st.session_state.employees)
        st.dataframe(employees_df)

# --- Process Payroll ---
elif option == "Process Payroll":
    st.subheader("Process Payroll")
    st.write(f"Calculate payroll for {pay_period_start} to {pay_period_end}.")

    if not st.session_state.employees:
        st.warning("No employees added. Go to 'Manage Employees' first.")
    else:
        # Tax and Deduction Rates (Simplified)
        fed_tax_rate = st.slider("Federal Tax Rate (%)", 0.0, 50.0, 15.0) / 100
        state_tax_rate = st.slider("State Tax Rate (%)", 0.0, 20.0, 5.0) / 100
        insurance_deduction = st.number_input("Insurance Deduction per Employee ($)", min_value=0.0, value=50.0)
        employer_tax_rate = st.slider("Employer Payroll Tax Rate (%)", 0.0, 20.0, 7.65) / 100  # e.g., Social Security/Medicare

        if st.button("Run Payroll"):
            payroll_data = []
            for emp in st.session_state.employees:
                # Calculate Gross Pay
                if emp["Pay Type"] == "Hourly":
                    gross_pay = emp["Rate"] * emp["Hours per Period"]
                else:
                    gross_pay = emp["Rate"] / 24  # Assuming semi-monthly pay (24 periods/year)

                # Deductions
                fed_tax = gross_pay * fed_tax_rate
                state_tax = gross_pay * state_tax_rate
                total_deductions = fed_tax + state_tax + insurance_deduction
                net_pay = gross_pay - total_deductions

                # Employer Costs
                employer_taxes = gross_pay * employer_tax_rate

                payroll_entry = {
                    "Employee ID": emp["Employee ID"],
                    "Name": emp["Name"],
                    "Gross Pay": gross_pay,
                    "Federal Tax": fed_tax,
                    "State Tax": state_tax,
                    "Insurance": insurance_deduction,
                    "Net Pay": net_pay,
                    "Employer Taxes": employer_taxes,
                    "Pay Period Start": pay_period_start,
                    "Pay Period End": pay_period_end
                }
                payroll_data.append(payroll_entry)

            st.session_state.payroll_records.extend(payroll_data)
            st.success(f"Payroll processed for {len(payroll_data)} employees!")

        # Display Latest Payroll
        if st.session_state.payroll_records:
            st.write("### Latest Payroll Run")
            payroll_df = pd.DataFrame(st.session_state.payroll_records[-len(st.session_state.employees):])
            st.dataframe(payroll_df)

# --- Payroll Ledger ---
elif option == "Payroll Ledger":
    st.subheader("Payroll Ledger")
    st.write("View all payroll transactions recorded.")

    if st.session_state.payroll_records:
        ledger_df = pd.DataFrame(st.session_state.payroll_records)
        filtered_df = ledger_df[
            (ledger_df["Pay Period Start"] >= pay_period_start) & 
            (ledger_df["Pay Period End"] <= pay_period_end)
        ]
        st.dataframe(filtered_df)
    else:
        st.write("No payroll records yet. Process payroll first.")

# --- Financial Impact ---
elif option == "Financial Impact":
    st.subheader("Financial Impact")
    st.write("Record payroll in the accounting system using double-entry.")

    if st.session_state.payroll_records:
        ledger_df = pd.DataFrame(st.session_state.payroll_records)
        filtered_df = ledger_df[
            (ledger_df["Pay Period Start"] >= pay_period_start) & 
            (ledger_df["Pay Period End"] <= pay_period_end)
        ]

        # Calculate Totals
        total_gross_pay = filtered_df["Gross Pay"].sum()
        total_fed_tax = filtered_df["Federal Tax"].sum()
        total_state_tax = filtered_df["State Tax"].sum()
        total_insurance = filtered_df["Insurance"].sum()
        total_net_pay = filtered_df["Net Pay"].sum()
        total_employer_taxes = filtered_df["Employer Taxes"].sum()

        # Journal Entry
        st.write("### Journal Entry")
        journal = [
            {"Account": "Salaries Expense", "Debit": total_gross_pay + total_employer_taxes, "Credit": 0.0},
            {"Account": "Cash", "Debit": 0.0, "Credit": total_net_pay},
            {"Account": "Federal Tax Payable", "Debit": 0.0, "Credit": total_fed_tax},
            {"Account": "State Tax Payable", "Debit": 0.0, "Credit": total_state_tax},
            {"Account": "Insurance Payable", "Debit": 0.0, "Credit": total_insurance},
            {"Account": "Employer Taxes Payable", "Debit": 0.0, "Credit": total_employer_taxes}
        ]
        journal_df = pd.DataFrame(journal)
        st.table(journal_df)

        # Balance Check
        total_debits = journal_df["Debit"].sum()
        total_credits = journal_df["Credit"].sum()
        if abs(total_debits - total_credits) < 0.01:
            st.success("Journal entry balances!")
        else:
            st.error("Journal entry does not balance!")

# --- Reports & Visualization ---
elif option == "Reports & Visualization":
    st.subheader("Reports & Visualization")
    st.write("Analyze payroll data.")

    if st.session_state.payroll_records:
        ledger_df = pd.DataFrame(st.session_state.payroll_records)
        filtered_df = ledger_df[
            (ledger_df["Pay Period Start"] >= pay_period_start) & 
            (ledger_df["Pay Period End"] <= pay_period_end)
        ]

        # Summary Report
        st.write("### Payroll Summary")
        summary = {
            "Total Gross Pay": filtered_df["Gross Pay"].sum(),
            "Total Federal Tax": filtered_df["Federal Tax"].sum(),
            "Total State Tax": filtered_df["State Tax"].sum(),
            "Total Insurance": filtered_df["Insurance"].sum(),
            "Total Net Pay": filtered_df["Net Pay"].sum(),
            "Total Employer Taxes": filtered_df["Employer Taxes"].sum()
        }
        summary_df = pd.DataFrame.from_dict(summary, orient="index", columns=["Amount"])
        st.table(summary_df)

        # Visualization
        st.write("### Cost Breakdown")
        fig, ax = plt.subplots()
        costs = [summary["Total Gross Pay"], summary["Total Employer Taxes"], summary["Total Federal Tax"] + summary["Total State Tax"]]
        labels = ["Gross Pay", "Employer Taxes", "Employee Taxes"]
        ax.bar(labels, costs, color=["#4CAF50", "#2196F3", "#FF5722"])
        ax.set_ylabel("Amount ($)")
        ax.set_title("Payroll Cost Breakdown")
        st.pyplot(fig)

        # Pie Chart
        st.write("### Deductions Distribution")
        fig2, ax2 = plt.subplots()
        deductions = [summary["Total Federal Tax"], summary["Total State Tax"], summary["Total Insurance"]]
        ded_labels = ["Federal Tax", "State Tax", "Insurance"]
        ax2.pie(deductions, labels=ded_labels, autopct="%1.1f%%", startangle=90)
        ax2.axis("equal")
        st.pyplot(fig2)
    else:
        st.write("No payroll data for reports.")

# Sidebar Info
st.sidebar.write("**Sample Employees:**")
st.sidebar.write("- ID: EMP001, Name: John Doe, Hourly, $20/hr, 80 hrs")
st.sidebar.write("- ID: EMP002, Name: Jane Smith, Salary, $50,000/yr")
if st.sidebar.button("Reset Data"):
    st.session_state.employees = []
    st.session_state.payroll_records = []
    st.sidebar.success("All data reset!")

# Footer
st.write("Built with Streamlit by Grok 3 (xAI)")
