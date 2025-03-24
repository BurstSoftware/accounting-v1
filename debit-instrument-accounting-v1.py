import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="Debit Instrument Accounting", layout="wide")

# Title and Introduction
st.title("Debit Instrument Accounting")
st.write("""
This app manages transactions for a debit instrument (e.g., checking account, debit card), tracking:
- **Debits**: Withdrawals or payments reducing the account balance (e.g., purchases, fees).
- **Credits**: Deposits or additions increasing the balance (e.g., income, refunds).
- Accounting entries to reflect these in the financial system.
- Balance tracking and financial impact analysis.
""")
st.write("Use this tool to simulate debit account usage and its accounting implications.")

# Initialize Session State
if "debit_transactions" not in st.session_state:
    st.session_state.debit_transactions = []
if "starting_balance" not in st.session_state:
    st.session_state.starting_balance = 10000.0

# Sidebar Navigation and Settings
st.sidebar.title("Debit Tools")
option = st.sidebar.selectbox(
    "Choose a Task",
    ["Setup Debit Instrument", "Record Transactions", "Transaction Ledger", "Accounting Entries", "Balance & Analysis"]
)
period_start = st.sidebar.date_input("Period Start", value=datetime(2025, 3, 1))
period_end = st.sidebar.date_input("Period End", value=datetime(2025, 3, 31))
starting_balance = st.sidebar.number_input("Starting Balance ($)", min_value=0.0, value=st.session_state.starting_balance)
st.session_state.starting_balance = starting_balance

# --- Setup Debit Instrument ---
if option == "Setup Debit Instrument":
    st.subheader("Setup Debit Instrument")
    st.write("Define the debit instrument’s details.")

    with st.form(key="debit_setup_form"):
        instrument_type = st.selectbox("Instrument Type", ["Checking Account", "Debit Card", "Savings Account"])
        overdraft_limit = st.number_input("Overdraft Limit ($)", min_value=0.0, value=500.0, help="Max allowable negative balance")
        submit_button = st.form_submit_button(label="Save Setup")

    if submit_button:
        st.session_state.debit_instrument = {
            "Type": instrument_type,
            "Overdraft Limit": overdraft_limit,
            "Starting Balance": st.session_state.starting_balance
        }
        st.success(f"Debit instrument setup: {instrument_type} with ${st.session_state.starting_balance:.2f} starting balance and ${overdraft_limit:.2f} overdraft limit.")

    # Display Current Setup
    if "debit_instrument" in st.session_state:
        st.write("### Current Debit Instrument")
        st.write(f"**Type**: {st.session_state.debit_instrument['Type']}")
        st.write(f"**Starting Balance**: ${st.session_state.debit_instrument['Starting Balance']:.2f}")
        st.write(f"**Overdraft Limit**: ${st.session_state.debit_instrument['Overdraft Limit']:.2f}")

# --- Record Transactions ---
elif option == "Record Transactions":
    st.subheader("Record Transactions")
    st.write("Add debits (withdrawals) or credits (deposits) to the debit instrument.")

    if "debit_instrument" not in st.session_state:
        st.warning("Setup the debit instrument first!")
    else:
        with st.form(key="transaction_form"):
            date = st.date_input("Date", value=datetime(2025, 3, 23), min_value=period_start, max_value=period_end)
            trans_type = st.selectbox("Transaction Type", ["Withdrawal (Debit)", "Deposit (Credit)", "Bank Fee"])
            amount = st.number_input("Amount ($)", min_value=0.0, value=100.0, step=10.0)
            description = st.text_input("Description", "e.g., Paid utilities")
            submit_button = st.form_submit_button(label="Record Transaction")

        if submit_button:
            current_balance = st.session_state.debit_instrument["Starting Balance"] + \
                              sum(t["Amount"] if t["Type"] == "Deposit (Credit)" else -t["Amount"] 
                                  for t in st.session_state.debit_transactions)
            new_balance = current_balance + (amount if trans_type == "Deposit (Credit)" else -amount)
            
            if new_balance < -st.session_state.debit_instrument["Overdraft Limit"] and trans_type in ["Withdrawal (Debit)", "Bank Fee"]:
                st.error(f"Transaction exceeds overdraft limit! Current balance: ${current_balance:.2f}, Overdraft limit: ${st.session_state.debit_instrument['Overdraft Limit']:.2f}")
            else:
                transaction = {
                    "Date": date,
                    "Type": trans_type,
                    "Description": description,
                    "Amount": amount,
                    "Balance After": new_balance
                }
                st.session_state.debit_transactions.append(transaction)
                st.success(f"Recorded: {description} - ${amount:.2f} ({trans_type})")

# --- Transaction Ledger ---
elif option == "Transaction Ledger":
    st.subheader("Transaction Ledger")
    st.write("View all transactions for the debit instrument.")

    if st.session_state.debit_transactions:
        ledger_df = pd.DataFrame(st.session_state.debit_transactions)
        filtered_df = ledger_df[
            (ledger_df["Date"] >= period_start) & (ledger_df["Date"] <= period_end)
        ]
        st.dataframe(filtered_df)

        # Running Balance
        st.write("### Running Balance")
        opening_balance = st.session_state.debit_instrument["Starting Balance"] if "debit_instrument" in st.session_state else st.session_state.starting_balance
        filtered_df["Running Balance"] = opening_balance + filtered_df["Amount"].cumsum() * \
                                        filtered_df["Type"].apply(lambda x: 1 if x == "Deposit (Credit)" else -1)
        st.line_chart(filtered_df.set_index("Date")[["Running Balance"]])
    else:
        st.write("No transactions recorded yet.")

# --- Accounting Entries ---
elif option == "Accounting Entries":
    st.subheader("Accounting Entries")
    st.write("Generate double-entry journal entries for debit instrument transactions.")

    if st.session_state.debit_transactions and "debit_instrument" in st.session_state:
        ledger_df = pd.DataFrame(st.session_state.debit_transactions)
        filtered_df = ledger_df[
            (ledger_df["Date"] >= period_start) & (ledger_df["Date"] <= period_end)
        ]

        # Journal Entries
        st.write("### Journal Entries")
        journal = []
        for _, row in filtered_df.iterrows():
            if row["Type"] == "Withdrawal (Debit)":
                journal.append({"Date": row["Date"], "Account": "Expense (e.g., Utilities)", "Debit": row["Amount"], "Credit": 0.0})
                journal.append({"Date": row["Date"], "Account": "Cash", "Debit": 0.0, "Credit": row["Amount"]})
            elif row["Type"] == "Deposit (Credit)":
                journal.append({"Date": row["Date"], "Account": "Cash", "Debit": row["Amount"], "Credit": 0.0})
                journal.append({"Date": row["Date"], "Account": "Revenue (e.g., Sales)", "Debit": 0.0, "Credit": row["Amount"]})
            elif row["Type"] == "Bank Fee":
                journal.append({"Date": row["Date"], "Account": "Bank Fee Expense", "Debit": row["Amount"], "Credit": 0.0})
                journal.append({"Date": row["Date"], "Account": "Cash", "Debit": 0.0, "Credit": row["Amount"]})

        journal_df = pd.DataFrame(journal)
        st.table(journal_df.groupby(["Date", "Account"]).sum().reset_index())

        # Balance Check
        total_debits = journal_df["Debit"].sum()
        total_credits = journal_df["Credit"].sum()
        if abs(total_debits - total_credits) < 0.01:
            st.success("Journal entries balance!")
        else:
            st.error("Journal entries do not balance!")
    else:
        st.write("Record transactions and setup the instrument first.")

# --- Balance & Analysis ---
elif option == "Balance & Analysis":
    st.subheader("Balance & Analysis")
    st.write("Track debit account balance and analyze usage.")

    if st.session_state.debit_transactions and "debit_instrument" in st.session_state:
        ledger_df = pd.DataFrame(st.session_state.debit_transactions)
        filtered_df = ledger_df[
            (ledger_df["Date"] >= period_start) & (ledger_df["Date"] <= period_end)
        ]

        # Current Balance
        opening_balance = st.session_state.debit_instrument["Starting Balance"]
        total_deposits = filtered_df[filtered_df["Type"] == "Deposit (Credit)"]["Amount"].sum()
        total_withdrawals = filtered_df[filtered_df["Type"] == "Withdrawal (Debit)"]["Amount"].sum()
        total_fees = filtered_df[filtered_df["Type"] == "Bank Fee"]["Amount"].sum()
        current_balance = opening_balance + total_deposits - total_withdrawals - total_fees

        st.write("### Account Summary")
        summary = {
            "Starting Balance": opening_balance,
            "Total Deposits": total_deposits,
            "Total Withdrawals": total_withdrawals,
            "Total Bank Fees": total_fees,
            "Current Balance": current_balance,
            "Overdraft Limit": -st.session_state.debit_instrument["Overdraft Limit"]
        }
        summary_df = pd.DataFrame.from_dict(summary, orient="index", columns=["Amount"])
        st.table(summary_df)

        # Balance Check
        if current_balance < -st.session_state.debit_instrument["Overdraft Limit"]:
            st.error("Balance below overdraft limit!")
        elif current_balance < 0:
            st.warning("Balance is negative but within overdraft limit.")
        else:
            st.success("Balance is positive.")

        # Visualization
        st.write("### Balance Over Time")
        filtered_df["Balance"] = opening_balance + filtered_df["Amount"].cumsum() * \
                                filtered_df["Type"].apply(lambda x: 1 if x == "Deposit (Credit)" else -1)
        fig, ax = plt.subplots()
        filtered_df.plot(x="Date", y="Balance", kind="line", ax=ax, marker="o", color="#2196F3")
        ax.axhline(0, color="black", linestyle="--", label="Zero Balance")
        ax.axhline(-st.session_state.debit_instrument["Overdraft Limit"], color="red", linestyle="--", label="Overdraft Limit")
        ax.set_ylabel("Balance ($)")
        ax.set_title("Debit Balance Trend")
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("No data for analysis. Setup and record transactions first.")

# Sidebar Info
st.sidebar.write("**Sample Transactions:**")
st.sidebar.write("- Withdrawal (Debit): $200, Paid utilities")
st.sidebar.write("- Deposit (Credit): $500, Sales revenue")
st.sidebar.write("- Bank Fee: $10, Monthly fee")
if st.sidebar.button("Reset Data"):
    st.session_state.debit_transactions = []
    if "debit_instrument" in st.session_state:
        del st.session_state.debit_instrument
    st.sidebar.success("All data reset!")

# Footer
st.write("Built with Streamlit by Nathan Rossow at(Burst Software)")
