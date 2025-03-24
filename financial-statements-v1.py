import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Financial Statements", layout="wide")

# Title and Introduction
st.title("Financial Statements")
st.write("""
Financial statements are reports that summarize a business’s financial performance and position. They include:
- **Balance Sheet**: A snapshot of assets, liabilities, and equity at a specific time.
- **Income Statement**: Shows revenue, expenses, and profit/loss over a period.
- **Cash Flow Statement**: Tracks cash inflows and outflows (operations, investing, financing) over a period.
""")

# Tabs for Each Statement
tab1, tab2, tab3 = st.tabs(["Balance Sheet", "Income Statement", "Cash Flow Statement"])

# --- Balance Sheet ---
with tab1:
    st.subheader("Balance Sheet")
    st.write("""
    The Balance Sheet reflects what a company owns (assets), owes (liabilities), and the owners’ stake (equity) at a specific date. It follows the equation: **Assets = Liabilities + Equity**.
    """)

    # Sample Data
    st.write("### Sample Balance Sheet (Editable)")
    date = st.date_input("As of Date", value=datetime(2025, 3, 23))

    # Assets
    st.write("#### Assets")
    cash = st.number_input("Cash", min_value=0.0, value=10000.0)
    accounts_receivable = st.number_input("Accounts Receivable", min_value=0.0, value=5000.0)
    inventory = st.number_input("Inventory", min_value=0.0, value=3000.0)
    equipment = st.number_input("Equipment", min_value=0.0, value=8000.0)
    total_assets = cash + accounts_receivable + inventory + equipment

    # Liabilities
    st.write("#### Liabilities")
    accounts_payable = st.number_input("Accounts Payable", min_value=0.0, value=4000.0)
    loans = st.number_input("Loans", min_value=0.0, value=6000.0)
    total_liabilities = accounts_payable + loans

    # Equity
    st.write("#### Equity")
    capital = st.number_input("Owner’s Capital", min_value=0.0, value=8000.0)
    retained_earnings = st.number_input("Retained Earnings", min_value=0.0, value=2000.0)
    total_equity = capital + retained_earnings

    # Display Balance Sheet
    balance_sheet = {
        "Assets": {"Cash": cash, "Accounts Receivable": accounts_receivable, "Inventory": inventory, "Equipment": equipment, "Total Assets": total_assets},
        "Liabilities": {"Accounts Payable": accounts_payable, "Loans": loans, "Total Liabilities": total_liabilities},
        "Equity": {"Owner’s Capital": capital, "Retained Earnings": retained_earnings, "Total Equity": total_equity}
    }
    balance_df = pd.DataFrame.from_dict(balance_sheet, orient="index").T
    st.table(balance_df)

    # Balance Check
    if total_assets == total_liabilities + total_equity:
        st.success(f"Balance Sheet balances as of {date}: Assets (${total_assets:.2f}) = Liabilities (${total_liabilities:.2f}) + Equity (${total_equity:.2f})")
    else:
        st.error(f"Balance Sheet does not balance! Assets (${total_assets:.2f}) ≠ Liabilities (${total_liabilities:.2f}) + Equity (${total_equity:.2f})")

    # Visualization
    st.write("### Visualization")
    fig, ax = plt.subplots()
    balance_data = [total_assets, total_liabilities, total_equity]
    labels = ["Total Assets", "Total Liabilities", "Total Equity"]
    ax.bar(labels, balance_data, color=["#4CAF50", "#FF5722", "#2196F3"])
    ax.set_ylabel("Amount ($)")
    ax.set_title(f"Balance Sheet Breakdown - {date}")
    st.pyplot(fig)

# --- Income Statement ---
with tab2:
    st.subheader("Income Statement")
    st.write("""
    The Income Statement (or Profit & Loss Statement) shows revenue, expenses, and net income over a period. It measures profitability: **Net Income = Revenue - Expenses**.
    """)

    # Period Selection
    st.write("### Sample Income Statement (Editable)")
    period_start = st.date_input("Period Start", value=datetime(2025, 1, 1))
    period_end = st.date_input("Period End", value=datetime(2025, 3, 23))

    # Revenue
    st.write("#### Revenue")
    sales = st.number_input("Sales Revenue", min_value=0.0, value=20000.0)
    other_income = st.number_input("Other Income", min_value=0.0, value=1000.0)
    total_revenue = sales + other_income

    # Expenses
    st.write("#### Expenses")
    cost_of_goods = st.number_input("Cost of Goods Sold", min_value=0.0, value=8000.0)
    rent = st.number_input("Rent Expense", min_value=0.0, value=2000.0)
    salaries = st.number_input("Salaries Expense", min_value=0.0, value=5000.0)
    total_expenses = cost_of_goods + rent + salaries

    # Net Income
    net_income = total_revenue - total_expenses

    # Display Income Statement
    income_statement = {
        "Revenue": {"Sales": sales, "Other Income": other_income, "Total Revenue": total_revenue},
        "Expenses": {"Cost of Goods Sold": cost_of_goods, "Rent": rent, "Salaries": salaries, "Total Expenses": total_expenses},
        "Net Income": {"Net Income": net_income}
    }
    income_df = pd.DataFrame.from_dict(income_statement, orient="index").T
    st.table(income_df)

    # Profitability Check
    if net_income > 0:
        st.success(f"Net Income for {period_start} to {period_end}: ${net_income:.2f} (Profit)")
    elif net_income < 0:
        st.warning(f"Net Income for {period_start} to {period_end}: ${net_income:.2f} (Loss)")
    else:
        st.info(f"Net Income for {period_start} to {period_end}: ${net_income:.2f} (Break-even)")

    # Visualization
    st.write("### Visualization")
    fig, ax = plt.subplots()
    income_data = [total_revenue, total_expenses, net_income]
    labels = ["Total Revenue", "Total Expenses", "Net Income"]
    ax.bar(labels, income_data, color=["#4CAF50", "#FF5722", "#2196F3"])
    ax.set_ylabel("Amount ($)")
    ax.set_title(f"Income Statement - {period_start} to {period_end}")
    st.pyplot(fig)

# --- Cash Flow Statement ---
with tab3:
    st.subheader("Cash Flow Statement")
    st.write("""
    The Cash Flow Statement tracks cash inflows and outflows over a period, categorized into:
    - **Operating Activities**: Cash from core business operations.
    - **Investing Activities**: Cash from buying/selling assets.
    - **Financing Activities**: Cash from loans, equity, or dividends.
    """)

    # Period Selection
    st.write("### Sample Cash Flow Statement (Editable)")
    cash_period_start = st.date_input("Cash Flow Period Start", value=datetime(2025, 1, 1), key="cash_start")
    cash_period_end = st.date_input("Cash Flow Period End", value=datetime(2025, 3, 23), key="cash_end")

    # Operating Activities
    st.write("#### Operating Activities")
    cash_sales = st.number_input("Cash from Sales", min_value=0.0, value=15000.0)
    cash_paid_suppliers = st.number_input("Cash Paid to Suppliers", min_value=0.0, value=7000.0)
    cash_paid_operating = st.number_input("Cash Paid for Operating Expenses", min_value=0.0, value=3000.0)
    net_cash_operations = cash_sales - cash_paid_suppliers - cash_paid_operating

    # Investing Activities
    st.write("#### Investing Activities")
    equipment_purchase = st.number_input("Cash Paid for Equipment", min_value=0.0, value=2000.0)
    net_cash_investing = -equipment_purchase

    # Financing Activities
    st.write("#### Financing Activities")
    loan_received = st.number_input("Cash from Loans", min_value=0.0, value=3000.0)
    dividends_paid = st.number_input("Cash Paid for Dividends", min_value=0.0, value=1000.0)
    net_cash_financing = loan_received - dividends_paid

    # Total Cash Flow
    net_cash_flow = net_cash_operations + net_cash_investing + net_cash_financing
    beginning_cash = st.number_input("Beginning Cash Balance", min_value=0.0, value=5000.0)
    ending_cash = beginning_cash + net_cash_flow

    # Display Cash Flow Statement
    cash_flow_statement = {
        "Operating Activities": {"Cash from Sales": cash_sales, "Cash Paid to Suppliers": -cash_paid_suppliers, "Cash Paid for Operating": -cash_paid_operating, "Net Cash from Operations": net_cash_operations},
        "Investing Activities": {"Cash Paid for Equipment": -equipment_purchase, "Net Cash from Investing": net_cash_investing},
        "Financing Activities": {"Cash from Loans": loan_received, "Cash Paid for Dividends": -dividends_paid, "Net Cash from Financing": net_cash_financing},
        "Summary": {"Net Cash Flow": net_cash_flow, "Beginning Cash": beginning_cash, "Ending Cash": ending_cash}
    }
    cash_flow_df = pd.DataFrame.from_dict(cash_flow_statement, orient="index").T
    st.table(cash_flow_df)

    # Cash Flow Analysis
    st.write(f"Net Cash Flow for {cash_period_start} to {cash_period_end}: ${net_cash_flow:.2f}")
    st.write(f"Ending Cash Balance: ${ending_cash:.2f}")

    # Visualization
    st.write("### Visualization")
    fig, ax = plt.subplots()
    cash_data = [net_cash_operations, net_cash_investing, net_cash_financing, net_cash_flow]
    labels = ["Operations", "Investing", "Financing", "Net Cash Flow"]
    ax.bar(labels, cash_data, color=["#4CAF50", "#FF5722", "#2196F3", "#9C27B0"])
    ax.set_ylabel("Amount ($)")
    ax.set_title(f"Cash Flow Breakdown - {cash_period_start} to {cash_period_end}")
    st.pyplot(fig)

# Interconnection Note
st.subheader("How They Connect")
st.write("""
- **Net Income** from the Income Statement increases Retained Earnings on the Balance Sheet.
- **Ending Cash** from the Cash Flow Statement matches Cash on the Balance Sheet.
- Changes in assets/liabilities (Balance Sheet) often tie to cash flows (Cash Flow Statement).
""")

# Footer
st.write("Built with Streamlit by Grok 3 (xAI)")
