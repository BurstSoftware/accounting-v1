import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="Accounting", layout="wide")

# Title and Introduction
st.title("Accounting")
st.write("""
Accounting is the process of interpreting, summarizing, and analyzing financial transactions to provide insights for decision-making. It builds on recorded data (e.g., from bookkeeping) to:
- Produce financial statements (Balance Sheet, Income Statement, Cash Flow Statement).
- Apply principles like double-entry and accrual accounting.
- Offer financial analysis for stakeholders.
""")
st.write("This app simulates core accounting tasks with interactive tools.")

# Initialize Session State
if "transactions" not in st.session_state:
    st.session_state.transactions = []
if "period_start" not in st.session_state:
    st.session_state.period_start = datetime(2025, 1, 1)
if "period_end" not in st.session_state:
    st.session_state.period_end = datetime(2025, 3, 23)

# Sidebar Navigation
st.sidebar.title("Accounting Tools")
option = st.sidebar.selectbox(
    "Choose a Task",
    ["Enter Transactions", "General Ledger", "Financial Statements", "Financial Analysis", "Accounting Principles"]
)
period_start = st.sidebar.date_input("Period Start", value=st.session_state.period_start, key="period_start")
period_end = st.sidebar.date_input("Period End", value=st.session_state.period_end, key="period_end")
st.session_state.period_start = period_start
st.session_state.period_end = period_end

# --- Enter Transactions ---
if option == "Enter Transactions":
    st.subheader("Enter Transactions")
    st.write("Record financial events using the double-entry system.")

    with st.form(key="transaction_form"):
        date = st.date_input("Date", value=datetime(2025, 3, 23), min_value=period_start, max_value=period_end)
        description = st.text_input("Description", "e.g., Sold goods on credit")
        amount = st.number_input("Amount ($)", min_value=0.0, value=100.0, step=10.0)
        
        col1, col2 = st.columns(2)
        with col1:
            debit_account = st.selectbox(
                "Debit Account",
                ["Cash", "Accounts Receivable", "Inventory", "Equipment", "Rent Expense", "Salaries Expense"],
                help="Account increased"
            )
        with col2:
            credit_account = st.selectbox(
                "Credit Account",
                ["Cash", "Accounts Payable", "Sales Revenue", "Loans Payable", "Capital", "Retained Earnings"],
                help="Account decreased or source"
            )
        
        submit_button = st.form_submit_button(label="Record Transaction")

    if submit_button:
        if debit_account == credit_account:
            st.error("Debit and Credit accounts must be different!")
        elif date < period_start or date > period_end:
            st.error("Date must be within the selected period!")
        else:
            transaction = {
                "Date": date,
                "Description": description,
                "Debit Account": debit_account,
                "Debit Amount": amount,
                "Credit Account": credit_account,
                "Credit Amount": amount
            }
            st.session_state.transactions.append(transaction)
            st.success(f"Transaction recorded: {description} for ${amount:.2f}")

# --- General Ledger ---
elif option == "General Ledger":
    st.subheader("General Ledger")
    st.write("View all transactions recorded in the accounting period.")

    if st.session_state.transactions:
        ledger_df = pd.DataFrame(st.session_state.transactions)
        filtered_df = ledger_df[
            (ledger_df["Date"] >= period_start) & (ledger_df["Date"] <= period_end)
        ]
        st.dataframe(filtered_df)

        # Trial Balance
        st.write("### Trial Balance")
        accounts = {}
        for entry in filtered_df.to_dict("records"):
            debit_acc = entry["Debit Account"]
            credit_acc = entry["Credit Account"]
            accounts[debit_acc] = accounts.get(debit_acc, 0) + entry["Debit Amount"]
            accounts[credit_acc] = accounts.get(credit_acc, 0) - entry["Credit Amount"]
        
        trial_balance_df = pd.DataFrame(list(accounts.items()), columns=["Account", "Net Balance"])
        total_debits = filtered_df["Debit Amount"].sum()
        total_credits = filtered_df["Credit Amount"].sum()
        st.table(trial_balance_df)
        st.write(f"**Total Debits**: ${total_debits:.2f}")
        st.write(f"**Total Credits**: ${total_credits:.2f}")
        if abs(total_debits - total_credits) < 0.01:
            st.success("Trial Balance is balanced!")
        else:
            st.error("Trial Balance is not balanced!")
    else:
        st.write("No transactions recorded yet.")

# --- Financial Statements ---
elif option == "Financial Statements":
    st.subheader("Financial Statements")
    st.write("Generate key financial reports based on recorded transactions.")

    if st.session_state.transactions:
        ledger_df = pd.DataFrame(st.session_state.transactions)
        filtered_df = ledger_df[
            (ledger_df["Date"] >= period_start) & (ledger_df["Date"] <= period_end)
        ]

        # Income Statement
        st.write("### Income Statement")
        revenue = filtered_df[filtered_df["Credit Account"] == "Sales Revenue"]["Credit Amount"].sum()
        expenses = filtered_df[
            filtered_df["Debit Account"].isin(["Rent Expense", "Salaries Expense"])
        ]["Debit Amount"].sum()
        net_income = revenue - expenses
        income_data = {"Revenue": revenue, "Expenses": expenses, "Net Income": net_income}
        income_df = pd.DataFrame.from_dict(income_data, orient="index", columns=["Amount"])
        st.table(income_df)
        st.write(f"Period: {period_start} to {period_end}")
        if net_income > 0:
            st.success(f"Net Income: ${net_income:.2f} (Profit)")
        else:
            st.warning(f"Net Income: ${net_income:.2f} (Loss or Break-even)")

        # Balance Sheet
        st.write("### Balance Sheet")
        cash = (
            filtered_df[filtered_df["Debit Account"] == "Cash"]["Debit Amount"].sum() -
            filtered_df[filtered_df["Credit Account"] == "Cash"]["Credit Amount"].sum()
        )
        accounts_receivable = filtered_df[filtered_df["Debit Account"] == "Accounts Receivable"]["Debit Amount"].sum()
        inventory = filtered_df[filtered_df["Debit Account"] == "Inventory"]["Debit Amount"].sum()
        equipment = filtered_df[filtered_df["Debit Account"] == "Equipment"]["Debit Amount"].sum()
        total_assets = cash + accounts_receivable + inventory + equipment

        accounts_payable = filtered_df[filtered_df["Credit Account"] == "Accounts Payable"]["Credit Amount"].sum()
        loans_payable = filtered_df[filtered_df["Credit Account"] == "Loans Payable"]["Credit Amount"].sum()
        total_liabilities = accounts_payable + loans_payable

        capital = filtered_df[filtered_df["Credit Account"] == "Capital"]["Credit Amount"].sum()
        retained_earnings = net_income  # Simplified: assumes no prior retained earnings
        total_equity = capital + retained_earnings

        balance_data = {
            "Assets": {"Cash": cash, "Accounts Receivable": accounts_receivable, "Inventory": inventory, "Equipment": equipment, "Total Assets": total_assets},
            "Liabilities": {"Accounts Payable": accounts_payable, "Loans Payable": loans_payable, "Total Liabilities": total_liabilities},
            "Equity": {"Capital": capital, "Retained Earnings": retained_earnings, "Total Equity": total_equity}
        }
        balance_df = pd.DataFrame.from_dict(balance_data, orient="index").T
        st.table(balance_df)
        st.write(f"As of: {period_end}")
        if abs(total_assets - (total_liabilities + total_equity)) < 0.01:
            st.success("Balance Sheet balances!")
        else:
            st.error("Balance Sheet does not balance!")

        # Visualization
        st.write("### Visualization")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        income_df.plot(kind="bar", ax=ax1, color="#4CAF50")
        ax1.set_title("Income Statement")
        ax1.set_ylabel("Amount ($)")
        balance_totals = [total_assets, total_liabilities, total_equity]
        ax2.bar(["Assets", "Liabilities", "Equity"], balance_totals, color=["#4CAF50", "#FF5722", "#2196F3"])
        ax2.set_title("Balance Sheet")
        ax2.set_ylabel("Amount ($)")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write("Record transactions to generate statements.")

# --- Financial Analysis ---
elif option == "Financial Analysis":
    st.subheader("Financial Analysis")
    st.write("Analyze financial data for insights.")

    if st.session_state.transactions:
        ledger_df = pd.DataFrame(st.session_state.transactions)
        filtered_df = ledger_df[
            (ledger_df["Date"] >= period_start) & (ledger_df["Date"] <= period_end)
        ]

        revenue = filtered_df[filtered_df["Credit Account"] == "Sales Revenue"]["Credit Amount"].sum()
        expenses = filtered_df[
            filtered_df["Debit Account"].isin(["Rent Expense", "Salaries Expense"])
        ]["Debit Amount"].sum()
        net_income = revenue - expenses
        total_assets = (
            filtered_df[filtered_df["Debit Account"] == "Cash"]["Debit Amount"].sum() -
            filtered_df[filtered_df["Credit Account"] == "Cash"]["Credit Amount"].sum()
        ) + filtered_df[filtered_df["Debit Account"] == "Accounts Receivable"]["Debit Amount"].sum() + \
            filtered_df[filtered_df["Debit Account"] == "Inventory"]["Debit Amount"].sum() + \
            filtered_df[filtered_df["Debit Account"] == "Equipment"]["Debit Amount"].sum()

        # Key Metrics
        st.write("### Key Metrics")
        profit_margin = (net_income / revenue * 100) if revenue > 0 else 0
        st.write(f"**Profit Margin**: {profit_margin:.2f}% (Net Income / Revenue)")
        return_on_assets = (net_income / total_assets * 100) if total_assets > 0 else 0
        st.write(f"**Return on Assets (ROA)**: {return_on_assets:.2f}% (Net Income / Total Assets)")

        # Trend Visualization (Simplified)
        st.write("### Transaction Trend")
        daily_totals = filtered_df.groupby("Date")["Debit Amount"].sum()
        fig, ax = plt.subplots()
        daily_totals.plot(kind="line", ax=ax, marker="o", color="#2196F3")
        ax.set_title("Daily Transaction Totals")
        ax.set_ylabel("Amount ($)")
        st.pyplot(fig)
    else:
        st.write("No data for analysis. Add transactions first.")

# --- Accounting Principles ---
elif option == "Accounting Principles":
    st.subheader("Accounting Principles")
    st.write("Key principles applied in this app:")
    principles = {
        "Double-Entry": "Every transaction affects two accounts (debit and credit).",
        "Accrual Basis": "Revenue and expenses are recorded when earned/incurred, not when cash changes hands.",
        "Consistency": "Methods are applied uniformly for comparability.",
        "Materiality": "Focus on significant items impacting decisions.",
        "Going Concern": "Assumes the business will continue operating."
    }
    for principle, desc in principles.items():
        with st.expander(principle):
            st.write(desc)

# Sidebar Info
st.sidebar.write("**Sample Transactions:**")
st.sidebar.write("- Debit Cash $1,000, Credit Sales Revenue $1,000 (Cash sale)")
st.sidebar.write("- Debit Rent Expense $300, Credit Cash $300 (Rent payment)")
if st.sidebar.button("Reset Transactions"):
    st.session_state.transactions = []
    st.sidebar.success("Transactions reset!")

# Footer
st.write("Built with Streamlit by Nathan Rossow at (Burst Software)")
