import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Double-Entry System", layout="wide")

# Title and Introduction
st.title("Double-Entry System")
st.write("""
The double-entry system is the foundation of modern accounting. Every financial transaction affects at least two accounts, ensuring the accounting equation (Assets = Liabilities + Equity) remains balanced. Debits and credits are used to record these changes:
- **Debits**: Increase assets/expenses, decrease liabilities/equity/revenue.
- **Credits**: Increase liabilities/equity/revenue, decrease assets/expenses.
""")

# Detailed Explanation
st.subheader("How It Works")
st.write("""
1. **Two-Sided Impact**: For every transaction, there’s a debit in one account and a credit in another, equal in amount.
2. **Accounts Involved**: Common accounts include Cash, Equipment (Assets), Loans (Liabilities), Capital (Equity), Sales (Revenue), and Rent (Expenses).
3. **Balance Check**: Total debits must always equal total credits, verified via a trial balance.
""")
st.write("Let’s simulate transactions, track them in a ledger, and verify the balance.")

# Initialize Session State for Ledger
if "ledger" not in st.session_state:
    st.session_state.ledger = []

# Transaction Entry Form
st.subheader("Enter a Transaction")
with st.form(key="transaction_form"):
    st.write("Define your transaction below:")
    col1, col2 = st.columns(2)
    
    with col1:
        debit_account = st.selectbox(
            "Debit Account", 
            ["Cash", "Equipment", "Inventory", "Rent Expense", "Accounts Receivable"]
        )
        debit_amount = st.number_input("Debit Amount ($)", min_value=0.0, value=0.0, step=10.0)
    
    with col2:
        credit_account = st.selectbox(
            "Credit Account", 
            ["Cash", "Loans Payable", "Sales Revenue", "Capital", "Accounts Payable"]
        )
        credit_amount = st.number_input("Credit Amount ($)", min_value=0.0, value=0.0, step=10.0)
    
    description = st.text_input("Transaction Description", "e.g., Bought equipment with cash")
    submit_button = st.form_submit_button(label="Add Transaction")

# Process Transaction
if submit_button:
    if debit_amount != credit_amount:
        st.error("Debits must equal Credits! Please adjust the amounts.")
    elif debit_account == credit_account:
        st.error("Debit and Credit accounts must be different!")
    else:
        transaction = {
            "Description": description,
            "Debit Account": debit_account,
            "Debit Amount": debit_amount,
            "Credit Account": credit_account,
            "Credit Amount": credit_amount
        }
        st.session_state.ledger.append(transaction)
        st.success("Transaction added successfully!")

# Display Ledger
st.subheader("Ledger")
if st.session_state.ledger:
    ledger_df = pd.DataFrame(st.session_state.ledger)
    st.table(ledger_df)
else:
    st.write("No transactions recorded yet.")

# Trial Balance Calculation
st.subheader("Trial Balance")
if st.session_state.ledger:
    accounts = {}
    for entry in st.session_state.ledger:
        # Update debit account
        debit_acc = entry["Debit Account"]
        if debit_acc in accounts:
            accounts[debit_acc] += entry["Debit Amount"]
        else:
            accounts[debit_acc] = entry["Debit Amount"]
        # Update credit account
        credit_acc = entry["Credit Account"]
        if credit_acc in accounts:
            accounts[credit_acc] -= entry["Credit Amount"]
        else:
            accounts[credit_acc] = -entry["Credit Amount"]

    trial_balance_df = pd.DataFrame(
        list(accounts.items()), columns=["Account", "Net Balance"]
    )
    total_debits = sum(entry["Debit Amount"] for entry in st.session_state.ledger)
    total_credits = sum(entry["Credit Amount"] for entry in st.session_state.ledger)
    
    st.write("### Account Balances")
    st.table(trial_balance_df)
    
    st.write(f"**Total Debits**: ${total_debits:.2f}")
    st.write(f"**Total Credits**: ${total_credits:.2f}")
    
    if total_debits == total_credits:
        st.success("Trial Balance is balanced!")
    else:
        st.error("Trial Balance is not balanced! Check your entries.")

# Visualization
st.subheader("Visualization")
if st.session_state.ledger:
    fig, ax = plt.subplots()
    trial_balance_df.plot(kind="bar", x="Account", y="Net Balance", ax=ax, color="skyblue")
    ax.set_title("Net Balance by Account")
    ax.set_ylabel("Balance ($)")
    ax.axhline(0, color="black", linewidth=0.8)
    st.pyplot(fig)
else:
    st.write("Add transactions to see a visualization.")

# Example Transactions
st.subheader("Example Transactions")
st.write("""
Try these examples:
1. **Buy Equipment with Cash**: Debit Equipment $500, Credit Cash $500.
2. **Sell Goods for Cash**: Debit Cash $1,000, Credit Sales Revenue $1,000.
3. **Pay Rent**: Debit Rent Expense $300, Credit Cash $300.
""")

# Reset Button
if st.button("Reset Ledger"):
    st.session_state.ledger = []
    st.write("Ledger reset successfully!")

# Footer
st.write("Built with Streamlit by Grok 3 (xAI)")
