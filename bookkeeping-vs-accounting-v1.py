import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Bookkeeping vs. Accounting", layout="wide")

# Title and Introduction
st.title("Bookkeeping vs. Accounting")
st.write("""
- **Bookkeeping**: The process of recording daily financial transactions (e.g., sales, purchases) in a systematic way. It’s tactical and detail-oriented.
- **Accounting**: The broader process of interpreting, summarizing, and analyzing recorded data to produce financial reports and inform decisions. It’s strategic and analytical.
""")
st.write("This app demonstrates both processes and how they work together.")

# Tabs for Bookkeeping and Accounting
tab1, tab2, tab3 = st.tabs(["Bookkeeping", "Accounting", "Integration"])

# --- Bookkeeping Tab ---
with tab1:
    st.subheader("Bookkeeping: Recording Transactions")
    st.write("""
    Bookkeeping focuses on:
    - Entering transactions into a ledger.
    - Ensuring accuracy and completeness.
    - Providing raw data for accounting.
    """)

    # Initialize Ledger in Session State
    if "bookkeeping_ledger" not in st.session_state:
        st.session_state.bookkeeping_ledger = []

    # Transaction Entry
    st.write("### Record a Transaction")
    with st.form(key="bookkeeping_form"):
        date = st.date_input("Transaction Date", value=datetime(2025, 3, 23))
        description = st.text_input("Description", "e.g., Paid rent")
        amount = st.number_input("Amount ($)", min_value=0.0, value=100.0, step=10.0)
        trans_type = st.selectbox("Type", ["Income", "Expense", "Asset Purchase", "Liability Payment"])
        debit_account = st.selectbox("Debit Account", ["Cash", "Accounts Receivable", "Equipment", "Rent Expense"])
        credit_account = st.selectbox("Credit Account", ["Cash", "Accounts Payable", "Sales Revenue", "Loans Payable"])
        submit_button = st.form_submit_button(label="Add Transaction")

    if submit_button:
        if debit_account == credit_account:
            st.error("Debit and Credit accounts must be different!")
        else:
            transaction = {
                "Date": date,
                "Description": description,
                "Amount": amount,
                "Type": trans_type,
                "Debit Account": debit_account,
                "Credit Account": credit_account
            }
            st.session_state.bookkeeping_ledger.append(transaction)
            st.success(f"Transaction recorded: {description} for ${amount:.2f}")

    # Display Ledger
    st.write("### General Ledger")
    if st.session_state.bookkeeping_ledger:
        ledger_df = pd.DataFrame(st.session_state.bookkeeping_ledger)
        st.dataframe(ledger_df)
    else:
        st.write("No transactions recorded yet.")

    # Visualization
    st.write("### Transaction Breakdown")
    if st.session_state.bookkeeping_ledger:
        ledger_df = pd.DataFrame(st.session_state.bookkeeping_ledger)
        type_summary = ledger_df.groupby("Type")["Amount"].sum()
        fig, ax = plt.subplots()
        type_summary.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90)
        ax.set_title("Transactions by Type")
        ax.axis("equal")
        st.pyplot(fig)

# --- Accounting Tab ---
with tab2:
    st.subheader("Accounting: Analysis and Reporting")
    st.write("""
    Accounting uses bookkeeping data to:
    - Summarize financial performance (e.g., Income Statement).
    - Assess financial position (e.g., Balance Sheet).
    - Track cash movements (e.g., Cash Flow Statement).
    - Provide insights for decision-making.
    """)

    # Use Bookkeeping Data if Available
    if st.session_state.bookkeeping_ledger:
        ledger_df = pd.DataFrame(st.session_state.bookkeeping_ledger)

        # Simple Income Statement
        st.write("### Income Statement (Derived from Ledger)")
        revenue = ledger_df[ledger_df["Type"] == "Income"]["Amount"].sum()
        expenses = ledger_df[ledger_df["Type"] == "Expense"]["Amount"].sum()
        net_income = revenue - expenses
        income_data = {"Revenue": revenue, "Expenses": expenses, "Net Income": net_income}
        income_df = pd.DataFrame.from_dict(income_data, orient="index", columns=["Amount"])
        st.table(income_df)

        # Profitability Feedback
        if net_income > 0:
            st.success(f"Net Income: ${net_income:.2f} (Profit)")
        elif net_income < 0:
            st.warning(f"Net Income: ${net_income:.2f} (Loss)")
        else:
            st.info("Net Income: $0.00 (Break-even)")

        # Simple Balance Sheet
        st.write("### Balance Sheet (Derived from Ledger)")
        cash = sum(
            entry["Amount"] if entry["Debit Account"] == "Cash" else -entry["Amount"]
            for entry in st.session_state.bookkeeping_ledger
            if entry["Debit Account"] == "Cash" or entry["Credit Account"] == "Cash"
        )
        equipment = ledger_df[ledger_df["Debit Account"] == "Equipment"]["Amount"].sum()
        total_assets = cash + equipment
        liabilities = ledger_df[ledger_df["Type"] == "Liability Payment"]["Amount"].sum()
        equity = total_assets - liabilities

        balance_data = {
            "Assets": {"Cash": cash, "Equipment": equipment, "Total Assets": total_assets},
            "Liabilities & Equity": {"Liabilities": liabilities, "Equity": equity, "Total": liabilities + equity}
        }
        balance_df = pd.DataFrame.from_dict(balance_data, orient="index").T
        st.table(balance_df)

        # Balance Check
        if abs(total_assets - (liabilities + equity)) < 0.01:
            st.success("Balance Sheet balances!")
        else:
            st.error("Balance Sheet does not balance!")

        # Visualization
        st.write("### Financial Snapshot")
        fig, ax = plt.subplots()
        balance_totals = [total_assets, liabilities, equity]
        labels = ["Assets", "Liabilities", "Equity"]
        ax.bar(labels, balance_totals, color=["#4CAF50", "#FF5722", "#2196F3"])
        ax.set_ylabel("Amount ($)")
        ax.set_title("Balance Sheet Breakdown")
        st.pyplot(fig)
    else:
        st.write("Add transactions in the Bookkeeping tab to see accounting reports.")

# --- Integration Tab ---
with tab3:
    st.subheader("Integration: From Bookkeeping to Accounting")
    st.write("""
    - **Bookkeeping** provides the raw data (transactions).
    - **Accounting** transforms this data into meaningful reports.
    - Together, they ensure accurate financial tracking and strategic insights.
    """)

    st.write("### Workflow Example")
    st.write("""
    1. **Bookkeeping**: Record "Sold goods for $500 cash" (Debit Cash, Credit Sales Revenue).
    2. **Accounting**: 
       - Income Statement: Add $500 to Revenue, calculate Net Income.
       - Balance Sheet: Increase Cash (Asset) by $500, Equity by $500 (via Net Income).
    """)

    # Interactive Example
    st.write("### Try It Yourself")
    sample_amount = st.number_input("Enter a Sales Amount ($)", min_value=0.0, value=500.0)
    if st.button("Process Sample Transaction"):
        # Simulate Bookkeeping
        sample_transaction = {
            "Date": datetime(2025, 3, 23),
            "Description": "Sample Sale",
            "Amount": sample_amount,
            "Type": "Income",
            "Debit Account": "Cash",
            "Credit Account": "Sales Revenue"
        }
        sample_ledger = [sample_transaction]
        st.write("**Bookkeeping Entry:**")
        st.table(pd.DataFrame(sample_ledger))

        # Simulate Accounting
        sample_revenue = sample_amount
        sample_net_income = sample_revenue
        sample_cash = sample_amount
        sample_equity = sample_net_income
        st.write("**Accounting Output:**")
        st.write(f"- Income Statement: Revenue = ${sample_revenue:.2f}, Net Income = ${sample_net_income:.2f}")
        st.write(f"- Balance Sheet: Cash = ${sample_cash:.2f}, Equity = ${sample_equity:.2f}")

# Sidebar with Additional Info
st.sidebar.title("Quick Reference")
st.sidebar.write("""
- **Bookkeeping Tasks**: Data entry, ledger maintenance.
- **Accounting Tasks**: Financial statements, analysis, forecasting.
- **Key Difference**: Bookkeeping is recording; Accounting is interpreting.
""")
if st.sidebar.button("Reset Ledger"):
    st.session_state.bookkeeping_ledger = []
    st.sidebar.success("Ledger reset!")

# Footer
st.write("Built with Streamlit by Nathan Rossow at (Burst Software)")
