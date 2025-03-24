import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="Bookkeeping", layout="wide")

# Title and Introduction
st.title("Bookkeeping")
st.write("""
Bookkeeping is the process of recording a business’s daily financial transactions in an organized manner. It’s the foundation of accounting, focusing on:
- Tracking income, expenses, assets, and liabilities.
- Maintaining a **General Ledger** as the central record.
- Ensuring accuracy for later financial analysis and reporting.
""")

# Initialize Session State for Ledger
if "ledger" not in st.session_state:
    st.session_state.ledger = []

# Sidebar for Navigation and Settings
st.sidebar.title("Bookkeeping Tools")
option = st.sidebar.selectbox(
    "Choose an Action",
    ["Add Transaction", "View Ledger", "Categorize Transactions", "Summary Report", "Visualization"]
)

# --- Add Transaction ---
if option == "Add Transaction":
    st.subheader("Add a New Transaction")
    st.write("Record income, expenses, or other financial events here.")

    with st.form(key="transaction_form"):
        date = st.date_input("Transaction Date", value=datetime(2025, 3, 23))
        description = st.text_input("Description", "e.g., Sold goods to customer")
        
        # Transaction Type and Amount
        trans_type = st.selectbox("Transaction Type", ["Income", "Expense", "Asset Purchase", "Liability Payment"])
        amount = st.number_input("Amount ($)", min_value=0.0, value=100.0, step=10.0)
        
        # Accounts Involved
        col1, col2 = st.columns(2)
        with col1:
            debit_account = st.selectbox(
                "Debit Account",
                ["Cash", "Accounts Receivable", "Inventory", "Equipment", "Rent Expense", "Salaries Expense"],
                help="Account increased by this transaction"
            )
        with col2:
            credit_account = st.selectbox(
                "Credit Account",
                ["Cash", "Accounts Payable", "Sales Revenue", "Loans Payable", "Capital"],
                help="Account decreased or source of funds"
            )
        
        category = st.text_input("Category (optional)", "e.g., Sales, Operating Expenses")
        submit_button = st.form_submit_button(label="Record Transaction")

    if submit_button:
        if debit_account == credit_account:
            st.error("Debit and Credit accounts must be different!")
        else:
            transaction = {
                "Date": date,
                "Description": description,
                "Type": trans_type,
                "Amount": amount,
                "Debit Account": debit_account,
                "Credit Account": credit_account,
                "Category": category if category else "Uncategorized"
            }
            st.session_state.ledger.append(transaction)
            st.success(f"Transaction recorded: {description} for ${amount:.2f}")

# --- View Ledger ---
elif option == "View Ledger":
    st.subheader("General Ledger")
    st.write("This is the complete record of all transactions entered.")

    if st.session_state.ledger:
        ledger_df = pd.DataFrame(st.session_state.ledger)
        st.dataframe(ledger_df)

        # Filter by Date
        st.write("### Filter Ledger")
        min_date = min([entry["Date"] for entry in st.session_state.ledger])
        max_date = max([entry["Date"] for entry in st.session_state.ledger])
        date_range = st.date_input("Select Date Range", [min_date, max_date])
        if len(date_range) == 2:
            filtered_df = ledger_df[
                (ledger_df["Date"] >= date_range[0]) & (ledger_df["Date"] <= date_range[1])
            ]
            st.dataframe(filtered_df)
    else:
        st.write("No transactions recorded yet. Add some in the 'Add Transaction' section!")

# --- Categorize Transactions ---
elif option == "Categorize Transactions":
    st.subheader("Categorize Transactions")
    st.write("Assign or edit categories for better organization and reporting.")

    if st.session_state.ledger:
        ledger_df = pd.DataFrame(st.session_state.ledger)
        st.write("### Current Ledger with Categories")
        st.dataframe(ledger_df[["Date", "Description", "Amount", "Category"]])

        # Edit Category
        transaction_index = st.selectbox(
            "Select Transaction to Edit",
            range(len(st.session_state.ledger)),
            format_func=lambda x: st.session_state.ledger[x]["Description"]
        )
        new_category = st.text_input("New Category", st.session_state.ledger[transaction_index]["Category"])
        if st.button("Update Category"):
            st.session_state.ledger[transaction_index]["Category"] = new_category
            st.success(f"Category updated for '{st.session_state.ledger[transaction_index]['Description']}'")
    else:
        st.write("No transactions to categorize yet.")

# --- Summary Report ---
elif option == "Summary Report":
    st.subheader("Summary Report")
    st.write("A breakdown of transactions by type and category.")

    if st.session_state.ledger:
        ledger_df = pd.DataFrame(st.session_state.ledger)

        # Summary by Type
        st.write("### By Transaction Type")
        type_summary = ledger_df.groupby("Type")["Amount"].sum().reset_index()
        st.table(type_summary)

        # Summary by Category
        st.write("### By Category")
        category_summary = ledger_df.groupby("Category")["Amount"].sum().reset_index()
        st.table(category_summary)

        # Total Debits and Credits
        debit_total = sum(
            entry["Amount"] for entry in st.session_state.ledger
            if entry["Debit Account"] in ["Cash", "Accounts Receivable", "Inventory", "Equipment"]
        )
        credit_total = sum(
            entry["Amount"] for entry in st.session_state.ledger
            if entry["Credit Account"] in ["Cash", "Accounts Payable", "Sales Revenue", "Loans Payable"]
        )
        st.write(f"**Total Debits**: ${debit_total:.2f}")
        st.write(f"**Total Credits**: ${credit_total:.2f}")
        if abs(debit_total - credit_total) < 0.01:  # Allow for rounding errors
            st.success("Debits and Credits are balanced!")
        else:
            st.warning("Debits and Credits are not balanced. Check your entries.")
    else:
        st.write("No data available for a summary report.")

# --- Visualization ---
elif option == "Visualization":
    st.subheader("Visualization")
    st.write("Visualize your bookkeeping data.")

    if st.session_state.ledger:
        ledger_df = pd.DataFrame(st.session_state.ledger)

        # Pie Chart by Transaction Type
        st.write("### Transaction Types")
        type_summary = ledger_df.groupby("Type")["Amount"].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(type_summary, labels=type_summary.index, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

        # Bar Chart by Category
        st.write("### Categories")
        category_summary = ledger_df.groupby("Category")["Amount"].sum()
        fig2, ax2 = plt.subplots()
        category_summary.plot(kind="bar", ax=ax2, color="#4CAF50")
        ax2.set_ylabel("Total Amount ($)")
        ax2.set_title("Transactions by Category")
        st.pyplot(fig2)
    else:
        st.write("Add transactions to see visualizations.")

# Example Transactions
st.sidebar.subheader("Sample Transactions")
st.sidebar.write("""
Try these:
1. **Income**: Debit Cash $500, Credit Sales Revenue $500, Category: Sales
2. **Expense**: Debit Rent Expense $200, Credit Cash $200, Category: Operating Expenses
3. **Asset Purchase**: Debit Equipment $1,000, Credit Cash $1,000, Category: Capital Expenditure
""")

# Reset Ledger
if st.sidebar.button("Reset Ledger"):
    st.session_state.ledger = []
    st.sidebar.success("Ledger reset successfully!")

# Footer
st.write("Built with Streamlit by Grok 3 (xAI)")
