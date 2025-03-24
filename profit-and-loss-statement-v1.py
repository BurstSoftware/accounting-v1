import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="Profit and Loss Statement", layout="wide")

# Title and Introduction
st.title("Profit and Loss Statement")
st.write("""
The **Profit and Loss Statement (P&L)**, or Income Statement, shows a business’s revenues, expenses, and net profit or loss over a specific period. Key components include:
- **Revenue**: Income from sales or services.
- **Expenses**: Costs incurred (e.g., operating, administrative).
- **Net Income**: Revenue minus Expenses (Profit if positive, Loss if negative).
""")
st.write("This app lets you build and analyze a P&L statement interactively.")

# Initialize Session State
if "revenues" not in st.session_state:
    st.session_state.revenues = []
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Sidebar Navigation and Settings
st.sidebar.title("P&L Tools")
option = st.sidebar.selectbox(
    "Choose a Task",
    ["Enter Revenues", "Enter Expenses", "P&L Statement", "Analysis & Visualization"]
)
period_start = st.sidebar.date_input("Period Start", value=datetime(2025, 1, 1))
period_end = st.sidebar.date_input("Period End", value=datetime(2025, 3, 31))

# --- Enter Revenues ---
if option == "Enter Revenues":
    st.subheader("Enter Revenues")
    st.write("Record all income sources for the period.")

    with st.form(key="revenue_form"):
        date = st.date_input("Date", value=datetime(2025, 3, 23), min_value=period_start, max_value=period_end)
        description = st.text_input("Description", "e.g., Product sales")
        amount = st.number_input("Amount ($)", min_value=0.0, value=1000.0, step=100.0)
        category = st.selectbox("Category", ["Sales", "Services", "Other Income"])
        submit_button = st.form_submit_button(label="Add Revenue")

    if submit_button:
        revenue = {
            "Date": date,
            "Description": description,
            "Amount": amount,
            "Category": category
        }
        st.session_state.revenues.append(revenue)
        st.success(f"Revenue added: {description} - ${amount:.2f}")

    # Display Revenues
    if st.session_state.revenues:
        st.write("### Recorded Revenues")
        revenues_df = pd.DataFrame(st.session_state.revenues)
        filtered_df = revenues_df[
            (revenues_df["Date"] >= period_start) & (revenues_df["Date"] <= period_end)
        ]
        st.dataframe(filtered_df)

# --- Enter Expenses ---
elif option == "Enter Expenses":
    st.subheader("Enter Expenses")
    st.write("Record all costs incurred during the period.")

    with st.form(key="expense_form"):
        date = st.date_input("Date", value=datetime(2025, 3, 23), min_value=period_start, max_value=period_end)
        description = st.text_input("Description", "e.g., Rent payment")
        amount = st.number_input("Amount ($)", min_value=0.0, value=500.0, step=50.0)
        category = st.selectbox("Category", ["Cost of Goods Sold", "Operating Expenses", "Administrative Expenses", "Other Expenses"])
        submit_button = st.form_submit_button(label="Add Expense")

    if submit_button:
        expense = {
            "Date": date,
            "Description": description,
            "Amount": amount,
            "Category": category
        }
        st.session_state.expenses.append(expense)
        st.success(f"Expense added: {description} - ${amount:.2f}")

    # Display Expenses
    if st.session_state.expenses:
        st.write("### Recorded Expenses")
        expenses_df = pd.DataFrame(st.session_state.expenses)
        filtered_df = expenses_df[
            (expenses_df["Date"] >= period_start) & (expenses_df["Date"] <= period_end)
        ]
        st.dataframe(filtered_df)

# --- P&L Statement ---
elif option == "P&L Statement":
    st.subheader("Profit and Loss Statement")
    st.write(f"Generated for {period_start} to {period_end}")

    if not st.session_state.revenues and not st.session_state.expenses:
        st.warning("No revenues or expenses recorded yet. Add data in the respective sections.")
    else:
        # Filter Data by Period
        revenues_df = pd.DataFrame(st.session_state.revenues)
        expenses_df = pd.DataFrame(st.session_state.expenses)
        filtered_revenues = revenues_df[
            (revenues_df["Date"] >= period_start) & (revenues_df["Date"] <= period_end)
        ]
        filtered_expenses = expenses_df[
            (expenses_df["Date"] >= period_start) & (expenses_df["Date"] <= period_end)
        ]

        # Revenue Breakdown
        st.write("### Revenue")
        revenue_by_category = filtered_revenues.groupby("Category")["Amount"].sum()
        total_revenue = revenue_by_category.sum()
        revenue_dict = revenue_by_category.to_dict()
        revenue_dict["Total Revenue"] = total_revenue
        revenue_df = pd.DataFrame.from_dict(revenue_dict, orient="index", columns=["Amount"])
        st.table(revenue_df)

        # Expense Breakdown
        st.write("### Expenses")
        expense_by_category = filtered_expenses.groupby("Category")["Amount"].sum()
        total_expenses = expense_by_category.sum()
        expense_dict = expense_by_category.to_dict()
        expense_dict["Total Expenses"] = total_expenses
        expense_df = pd.DataFrame.from_dict(expense_dict, orient="index", columns=["Amount"])
        st.table(expense_df)

        # Net Income
        st.write("### Net Income")
        net_income = total_revenue - total_expenses
        net_income_df = pd.DataFrame({"Net Income": [net_income]}, index=["Result"])
        st.table(net_income_df)

        # Feedback
        if net_income > 0:
            st.success(f"Net Profit: ${net_income:.2f}")
        elif net_income < 0:
            st.warning(f"Net Loss: ${abs(net_income):.2f}")
        else:
            st.info("Break-even: $0.00")

        # Journal Entry (Simplified)
        st.write("### Accounting Entry (Accrual Basis)")
        journal = [
            {"Account": "Cash/Accounts Receivable", "Debit": total_revenue, "Credit": 0.0},
            {"Account": "Revenue", "Debit": 0.0, "Credit": total_revenue},
            {"Account": "Expenses", "Debit": total_expenses, "Credit": 0.0},
            {"Account": "Cash/Accounts Payable", "Debit": 0.0, "Credit": total_expenses}
        ]
        journal_df = pd.DataFrame(journal)
        st.table(journal_df)

# --- Analysis & Visualization ---
elif option == "Analysis & Visualization":
    st.subheader("Analysis & Visualization")
    st.write("Analyze your P&L data.")

    if not st.session_state.revenues and not st.session_state.expenses:
        st.write("No data for analysis. Add revenues and expenses first.")
    else:
        revenues_df = pd.DataFrame(st.session_state.revenues)
        expenses_df = pd.DataFrame(st.session_state.expenses)
        filtered_revenues = revenues_df[
            (revenues_df["Date"] >= period_start) & (revenues_df["Date"] <= period_end)
        ]
        filtered_expenses = expenses_df[
            (expenses_df["Date"] >= period_start) & (expenses_df["Date"] <= period_end)
        ]

        total_revenue = filtered_revenues["Amount"].sum()
        total_expenses = filtered_expenses["Amount"].sum()
        net_income = total_revenue - total_expenses

        # Breakdown by Category
        st.write("### Revenue by Category")
        revenue_by_category = filtered_revenues.groupby("Category")["Amount"].sum()
        st.table(revenue_by_category)

        st.write("### Expenses by Category")
        expense_by_category = filtered_expenses.groupby("Category")["Amount"].sum()
        st.table(expense_by_category)

        # Visualization
        st.write("### P&L Overview")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Bar Chart
        pl_data = {"Revenue": total_revenue, "Expenses": total_expenses, "Net Income": net_income}
        ax1.bar(pl_data.keys(), pl_data.values(), color=["#4CAF50", "#FF5722", "#2196F3"])
        ax1.set_ylabel("Amount ($)")
        ax1.set_title("P&L Summary")

        # Pie Chart for Expenses
        if total_expenses > 0:
            ax2.pie(expense_by_category, labels=expense_by_category.index, autopct="%1.1f%%", startangle=90)
            ax2.set_title("Expense Distribution")
            ax2.axis("equal")

        plt.tight_layout()
        st.pyplot(fig)

        # Trend Analysis (if multiple dates)
        if len(filtered_revenues["Date"].unique()) > 1 or len(filtered_expenses["Date"].unique()) > 1:
            st.write("### Trend Over Time")
            daily_revenue = filtered_revenues.groupby("Date")["Amount"].sum()
            daily_expenses = filtered_expenses.groupby("Date")["Amount"].sum()
            trend_df = pd.concat([daily_revenue, daily_expenses], axis=1).fillna(0)
            trend_df.columns = ["Revenue", "Expenses"]
            trend_df["Net Income"] = trend_df["Revenue"] - trend_df["Expenses"]
            
            fig2, ax = plt.subplots()
            trend_df.plot(ax=ax, marker="o")
            ax.set_ylabel("Amount ($)")
            ax.set_title("Daily P&L Trend")
            st.pyplot(fig2)

# Sidebar Info
st.sidebar.write("**Sample Entries:**")
st.sidebar.write("- Revenue: $1,000, Product sales, Sales")
st.sidebar.write("- Expense: $500, Rent payment, Operating Expenses")
if st.sidebar.button("Reset Data"):
    st.session_state.revenues = []
    st.session_state.expenses = []
    st.sidebar.success("All data reset!")

# Footer
st.write("Built with Streamlit by Grok 3 (xAI)")
