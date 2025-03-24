import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="Credit Instrument Accounting", layout="wide")

# Title and Introduction
st.title("Credit Instrument Accounting")
st.write("""
This app manages transactions for a credit instrument (e.g., credit card, loan, line of credit), tracking:
- **Debits**: Charges or payments reducing the credit balance (e.g., purchases, fees).
- **Credits**: Increases to the credit liability or payments reducing it (e.g., borrowing, repayments).
- Accounting entries to reflect these in the financial system.
- Balance tracking and financial impact analysis.
""")
st.write("Use this tool to simulate credit usage and its accounting implications.")

# Initialize Session State
if "credit_transactions" not in st.session_state:
    st.session_state.credit_transactions = []
if "credit_limit" not in st.session_state:
    st.session_state.credit_limit = 5000.0

# Sidebar Navigation and Settings
st.sidebar.title("Credit Tools")
option = st.sidebar.selectbox(
    "Choose a Task",
    ["Setup Credit Instrument", "Record Transactions", "Transaction Ledger", "Accounting Entries", "Balance & Analysis"]
)
period_start = st.sidebar.date_input("Period Start", value=datetime(2025, 3, 1))
period_end = st.sidebar.date_input("Period End", value=datetime(2025, 3, 31))
credit_limit = st.sidebar.number_input("Credit Limit ($)", min_value=0.0, value=st.session_state.credit_limit)
st.session_state.credit_limit = credit_limit

# --- Setup Credit Instrument ---
if option == "Setup Credit Instrument":
    st.subheader("Setup Credit Instrument")
    st.write("Define the credit instrument’s details.")

    with st.form(key="credit_setup_form"):
        instrument_type = st.selectbox("Instrument Type", ["Credit Card", "Line of Credit", "Loan"])
        interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0, step=0.1)
        opening_balance = st.number_input("Opening Balance ($)", min_value=0.0, value=0.0, help="Initial amount owed")
        submit_button = st.form_submit_button(label="Save Setup")

    if submit_button:
        st.session_state.credit_instrument = {
            "Type": instrument_type,
            "Interest Rate": interest_rate / 100,
            "Opening Balance": opening_balance
        }
        st.success(f"Credit instrument setup: {instrument_type} with ${opening_balance:.2f} opening balance and {interest_rate}% interest.")

    # Display Current Setup
    if "credit_instrument" in st.session_state:
        st.write("### Current Credit Instrument")
        st.write(f"**Type**: {st.session_state.credit_instrument['Type']}")
        st.write(f"**Interest Rate**: {st.session_state.credit_instrument['Interest Rate'] * 100:.2f}%")
        st.write(f"**Opening Balance**: ${st.session_state.credit_instrument['Opening Balance']:.2f}")
        st.write(f"**Credit Limit**: ${st.session_state.credit_limit:.2f}")

# --- Record Transactions ---
elif option == "Record Transactions":
    st.subheader("Record Transactions")
    st.write("Add debits (charges) or credits (repayments) to the credit instrument.")

    if "credit_instrument" not in st.session_state:
        st.warning("Setup the credit instrument first!")
    else:
        with st.form(key="transaction_form"):
            date = st.date_input("Date", value=datetime(2025, 3, 23), min_value=period_start, max_value=period_end)
            trans_type = st.selectbox("Transaction Type", ["Charge (Debit)", "Repayment (Credit)", "Interest Charge"])
            amount = st.number_input("Amount ($)", min_value=0.0, value=100.0, step=10.0)
            description = st.text_input("Description", "e.g., Purchased supplies")
            submit_button = st.form_submit_button(label="Record Transaction")

        if submit_button:
            current_balance = st.session_state.credit_instrument["Opening Balance"] + \
                              sum(t["Amount"] if t["Type"] in ["Charge (Debit)", "Interest Charge"] else -t["Amount"] 
                                  for t in st.session_state.credit_transactions)
            new_balance = current_balance + (amount if trans_type in ["Charge (Debit)", "Interest Charge"] else -amount)
            
            if new_balance > st.session_state.credit_limit and trans_type in ["Charge (Debit)", "Interest Charge"]:
                st.error(f"Transaction exceeds credit limit of ${st.session_state.credit_limit:.2f}! Current balance: ${current_balance:.2f}")
            else:
                transaction = {
                    "Date": date,
                    "Type": trans_type,
                    "Description": description,
                    "Amount": amount,
                    "Balance After": new_balance
                }
                st.session_state.credit_transactions.append(transaction)
                st.success(f"Recorded: {description} - ${amount:.2f} ({trans_type})")

# --- Transaction Ledger ---
elif option == "Transaction Ledger":
    st.subheader("Transaction Ledger")
    st.write("View all transactions for the credit instrument.")

    if st.session_state.credit_transactions:
        ledger_df = pd.DataFrame(st.session_state.credit_transactions)
        filtered_df = ledger_df[
            (ledger_df["Date"] >= period_start) & (ledger_df["Date"] <= period_end)
        ]
        st.dataframe(filtered_df)

        # Running Balance
        st.write("### Running Balance")
        opening_balance = st.session_state.credit_instrument["Opening Balance"] if "credit_instrument" in st.session_state else 0
        filtered_df["Running Balance"] = opening_balance + filtered_df["Amount"].cumsum() * \
                                        filtered_df["Type"].apply(lambda x: 1 if x in ["Charge (Debit)", "Interest Charge"] else -1)
        st.line_chart(filtered_df.set_index("Date")[["Running Balance"]])
    else:
        st.write("No transactions recorded yet.")

# --- Accounting Entries ---
elif option == "Accounting Entries":
    st.subheader("Accounting Entries")
    st.write("Generate double-entry journal entries for credit transactions.")

    if st.session_state.credit_transactions and "credit_instrument" in st.session_state:
        ledger_df = pd.DataFrame(st.session_state.credit_transactions)
        filtered_df = ledger_df[
            (ledger_df["Date"] >= period_start) & (ledger_df["Date"] <= period_end)
        ]

        # Journal Entries
        st.write("### Journal Entries")
        journal = []
        for _, row in filtered_df.iterrows():
            if row["Type"] == "Charge (Debit)":
                journal.append({"Date": row["Date"], "Account": "Expense (e.g., Supplies)", "Debit": row["Amount"], "Credit": 0.0})
                journal.append({"Date": row["Date"], "Account": "Credit Payable", "Debit": 0.0, "Credit": row["Amount"]})
            elif row["Type"] == "Repayment (Credit)":
                journal.append({"Date": row["Date"], "Account": "Credit Payable", "Debit": row["Amount"], "Credit": 0.0})
                journal.append({"Date": row["Date"], "Account": "Cash", "Debit": 0.0, "Credit": row["Amount"]})
            elif row["Type"] == "Interest Charge":
                journal.append({"Date": row["Date"], "Account": "Interest Expense", "Debit": row["Amount"], "Credit": 0.0})
                journal.append({"Date": row["Date"], "Account": "Credit Payable", "Debit": 0.0, "Credit": row["Amount"]})

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
    st.write("Track credit balance and analyze usage.")

    if st.session_state.credit_transactions and "credit_instrument" in st.session_state:
        ledger_df = pd.DataFrame(st.session_state.credit_transactions)
        filtered_df = ledger_df[
            (ledger_df["Date"] >= period_start) & (ledger_df["Date"] <= period_end)
        ]

        # Current Balance
        opening_balance = st.session_state.credit_instrument["Opening Balance"]
        total_charges = filtered_df[filtered_df["Type"] == "Charge (Debit)"]["Amount"].sum()
        total_interest = filtered_df[filtered_df["Type"] == "Interest Charge"]["Amount"].sum()
        total_repayments = filtered_df[filtered_df["Type"] == "Repayment (Credit)"]["Amount"].sum()
        current_balance = opening_balance + total_charges + total_interest - total_repayments

        st.write("### Credit Summary")
        summary = {
            "Opening Balance": opening_balance,
            "Total Charges": total_charges,
            "Total Interest": total_interest,
            "Total Repayments": total_repayments,
            "Current Balance": current_balance,
            "Credit Limit": st.session_state.credit_limit,
            "Available Credit": st.session_state.credit_limit - current_balance
        }
        summary_df = pd.DataFrame.from_dict(summary, orient="index", columns=["Amount"])
        st.table(summary_df)

        # Credit Utilization
        utilization = (current_balance / st.session_state.credit_limit * 100) if st.session_state.credit_limit > 0 else 0
        st.write(f"**Credit Utilization**: {utilization:.2f}%")
        if utilization > 80:
            st.warning("High utilization! Consider reducing balance.")

        # Visualization
        st.write("### Balance Over Time")
        filtered_df["Balance"] = opening_balance + filtered_df["Amount"].cumsum() * \
                                filtered_df["Type"].apply(lambda x: 1 if x in ["Charge (Debit)", "Interest Charge"] else -1)
        fig, ax = plt.subplots()
        filtered_df.plot(x="Date", y="Balance", kind="line", ax=ax, marker="o", color="#2196F3")
        ax.axhline(st.session_state.credit_limit, color="red", linestyle="--", label="Credit Limit")
        ax.set_ylabel("Balance ($)")
        ax.set_title("Credit Balance Trend")
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("No data for analysis. Setup and record transactions first.")

# Sidebar Info
st.sidebar.write("**Sample Transactions:**")
st.sidebar.write("- Charge (Debit): $200, Purchased supplies")
st.sidebar.write("- Repayment (Credit): $150, Payment to credit account")
st.sidebar.write("- Interest Charge: $10, Monthly interest")
if st.sidebar.button("Reset Data"):
    st.session_state.credit_transactions = []
    if "credit_instrument" in st.session_state:
        del st.session_state.credit_instrument
    st.sidebar.success("All data reset!")

# Footer
st.write("Built with Streamlit by Nathan Rossow at (Nathan Rossow)")
