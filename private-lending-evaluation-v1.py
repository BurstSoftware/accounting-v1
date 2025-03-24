import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Private Lending Evaluation", layout="wide")

# Title and Introduction
st.title("Private Lending Evaluation")
st.write("""
This app simulates a private lending institution’s evaluation process for personal loans. As a user, you can:
- Input your **monthly income**, **credit score**, and **desired loan amount**.
- See the lending outcome (Approved or Denied) based on banking criteria.
- View estimated loan terms (interest rate, monthly payment) if approved.
- Explore accounting implications for the lender.

**Evaluation Criteria:**
- **Debt-to-Income (DTI) Ratio**: Monthly debt payments (including new loan) / Monthly income (max 45%).
- **Credit Score**: Minimum 600 for consideration, impacts interest rate.
- **Loan Amount**: Assessed against income and creditworthiness.
""")

# Initialize Session State
if "loan_applications" not in st.session_state:
    st.session_state.loan_applications = []

# Sidebar Navigation
st.sidebar.title("Lending Tools")
option = st.sidebar.selectbox(
    "Choose a Task",
    ["Submit Loan Request", "View Applications", "Evaluation Outcome", "Accounting Entries", "Analysis & Visualization"]
)
evaluation_date = st.sidebar.date_input("Evaluation Date", value=datetime(2025, 3, 23))

# --- Submit Loan Request ---
if option == "Submit Loan Request":
    st.subheader("Submit Loan Request")
    st.write("Enter your financial details to request a loan.")

    with st.form(key="loan_form"):
        # User Info
        applicant_id = st.text_input("Applicant ID", "e.g., USER001")
        name = st.text_input("Your Name")
        
        # Financial Info
        monthly_income = st.number_input("Monthly Income ($)", min_value=0.0, value=4000.0, step=100.0)
        existing_debt_payments = st.number_input("Existing Monthly Debt Payments ($)", min_value=0.0, value=800.0, help="e.g., rent, car payments")
        credit_score = st.number_input("Credit Score (300-850)", min_value=300, max_value=850, value=650)

        # Loan Details
        loan_amount = st.number_input("Desired Loan Amount ($)", min_value=1000.0, value=10000.0, step=500.0)
        loan_term = st.selectbox("Loan Term (Years)", [1, 2, 3, 5, 7], index=2)

        submit_button = st.form_submit_button(label="Submit Request")

    if submit_button:
        if not applicant_id or not name:
            st.error("Applicant ID and Name are required!")
        elif monthly_income <= 0:
            st.error("Monthly income must be greater than zero!")
        else:
            application = {
                "Applicant ID": applicant_id,
                "Name": name,
                "Monthly Income": monthly_income,
                "Existing Debt Payments": existing_debt_payments,
                "Credit Score": credit_score,
                "Loan Amount": loan_amount,
                "Loan Term": loan_term,
                "Date Submitted": evaluation_date,
                "Status": "Pending"
            }
            st.session_state.loan_applications.append(application)
            st.success(f"Loan request submitted for {name} - ${loan_amount:.2f}")

    # Display Submitted Requests
    if st.session_state.loan_applications:
        st.write("### Your Submitted Requests")
        apps_df = pd.DataFrame(st.session_state.loan_applications)
        st.dataframe(apps_df[apps_df["Date Submitted"] == evaluation_date])

# --- View Applications ---
elif option == "View Applications":
    st.subheader("View Applications")
    st.write("See all loan requests submitted on the evaluation date.")

    if st.session_state.loan_applications:
        apps_df = pd.DataFrame(st.session_state.loan_applications)
        filtered_df = apps_df[apps_df["Date Submitted"] == evaluation_date]
        st.dataframe(filtered_df)
    else:
        st.write("No loan requests submitted yet.")

# --- Evaluation Outcome ---
elif option == "Evaluation Outcome":
    st.subheader("Evaluation Outcome")
    st.write("Review the lending institution’s decision on your loan request.")

    if not st.session_state.loan_applications:
        st.warning("No applications to evaluate. Submit a request first.")
    else:
        apps_df = pd.DataFrame(st.session_state.loan_applications)
        pending_df = apps_df[apps_df["Status"] == "Pending"]

        if pending_df.empty:
            st.write("No pending applications to evaluate.")
        else:
            selected_app = st.selectbox(
                "Select Your Application",
                pending_df.index,
                format_func=lambda x: f"{pending_df.loc[x, 'Name']} - ${pending_df.loc[x, 'Loan Amount']:.2f}"
            )
            app = pending_df.loc[selected_app]

            # Calculate Interest Rate Based on Credit Score
            if app["Credit Score"] >= 750:
                interest_rate = 5.0  # Excellent credit
            elif app["Credit Score"] >= 700:
                interest_rate = 6.5  # Good credit
            elif app["Credit Score"] >= 650:
                interest_rate = 8.0  # Fair credit
            elif app["Credit Score"] >= 600:
                interest_rate = 10.0  # Poor credit
            else:
                interest_rate = None  # Denied

            # Calculate Monthly Payment
            if interest_rate:
                monthly_rate = interest_rate / 1200
                months = app["Loan Term"] * 12
                monthly_payment = (app["Loan Amount"] * monthly_rate) / (1 - (1 + monthly_rate) ** -months)
            else:
                monthly_payment = 0.0

            # DTI Calculation
            total_debt_payments = app["Existing Debt Payments"] + monthly_payment
            dti_ratio = (total_debt_payments / app["Monthly Income"]) * 100 if app["Monthly Income"] > 0 else 100

            # Evaluation Criteria
            dti_threshold = 45.0  # Max DTI
            credit_threshold = 600  # Min credit score
            max_loan_to_income = 5.0  # Loan amount max 5x annual income

            st.write("### Your Application Details")
            st.write(f"**Name**: {app['Name']}")
            st.write(f"**Loan Amount**: ${app['Loan Amount']:.2f}")
            st.write(f"**Loan Term**: {app['Loan Term']} years")
            st.write(f"**Monthly Income**: ${app['Monthly Income']:.2f}")
            st.write(f"**Existing Debt Payments**: ${app['Existing Debt Payments']:.2f}")
            st.write(f"**Credit Score**: {app['Credit Score']}")

            st.write("### Lender’s Evaluation")
            issues = []
            if dti_ratio > dti_threshold:
                issues.append(f"DTI Ratio ({dti_ratio:.2f}%) exceeds threshold ({dti_threshold}%)")
            if app["Credit Score"] < credit_threshold:
                issues.append(f"Credit Score ({app['Credit Score']}) below threshold ({credit_threshold})")
            if app["Loan Amount"] > app["Monthly Income"] * 12 * max_loan_to_income:
                issues.append(f"Loan Amount exceeds {max_loan_to_income}x annual income (${app['Monthly Income'] * 12 * max_loan_to_income:.2f})")

            if not issues and interest_rate:
                st.success("Loan Approved!")
                st.write(f"**Estimated Interest Rate**: {interest_rate:.2f}%")
                st.write(f"**Estimated Monthly Payment**: ${monthly_payment:.2f}")
                st.session_state.loan_applications[selected_app]["Status"] = "Approved"
                st.session_state.loan_applications[selected_app]["Interest Rate"] = interest_rate / 100
                st.session_state.loan_applications[selected_app]["Monthly Payment"] = monthly_payment
            else:
                st.error("Loan Denied!")
                for issue in issues:
                    st.warning(issue)
                st.session_state.loan_applications[selected_app]["Status"] = "Denied"

# --- Accounting Entries ---
elif option == "Accounting Entries":
    st.subheader("Accounting Entries")
    st.write("View double-entry journal entries for approved loans from the lender’s perspective.")

    if st.session_state.loan_applications:
        apps_df = pd.DataFrame(st.session_state.loan_applications)
        approved_df = apps_df[apps_df["Status"] == "Approved"]

        if approved_df.empty:
            st.write("No approved loans to record.")
        else:
            st.write("### Journal Entries for Approved Loans")
            journal = []
            for _, app in approved_df.iterrows():
                journal.append({
                    "Date": app["Date Submitted"],
                    "Account": "Loans Receivable",
                    "Debit": app["Loan Amount"],
                    "Credit": 0.0
                })
                journal.append({
                    "Date": app["Date Submitted"],
                    "Account": "Cash",
                    "Debit": 0.0,
                    "Credit": app["Loan Amount"]
                })
            journal_df = pd.DataFrame(journal)
            st.table(journal_df.groupby(["Date", "Account"]).sum().reset_index())

            total_debits = journal_df["Debit"].sum()
            total_credits = journal_df["Credit"].sum()
            if abs(total_debits - total_credits) < 0.01:
                st.success("Journal entries balance!")
            else:
                st.error("Journal entries do not balance!")
    else:
        st.write("No applications processed yet.")

# --- Analysis & Visualization ---
elif option == "Analysis & Visualization":
    st.subheader("Analysis & Visualization")
    st.write("Review lending outcomes and trends.")

    if st.session_state.loan_applications:
        apps_df = pd.DataFrame(st.session_state.loan_applications)
        filtered_df = apps_df[apps_df["Date Submitted"] == evaluation_date]

        # Summary
        st.write("### Lending Summary")
        summary = {
            "Total Requests": len(filtered_df),
            "Approved": len(filtered_df[filtered_df["Status"] == "Approved"]),
            "Denied": len(filtered_df[filtered_df["Status"] == "Denied"]),
            "Pending": len(filtered_df[filtered_df["Status"] == "Pending"]),
            "Total Approved Amount": filtered_df[filtered_df["Status"] == "Approved"]["Loan Amount"].sum()
        }
        summary_df = pd.DataFrame.from_dict(summary, orient="index", columns=["Value"])
        st.table(summary_df)

        # Visualization
        st.write("### Outcome Distribution")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Pie Chart: Status
        status_counts = filtered_df["Status"].value_counts()
        ax1.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
        ax1.set_title("Loan Status Distribution")
        ax1.axis("equal")

        # Bar Chart: Loan Amounts by Status
        approved_amounts = filtered_df[filtered_df["Status"] == "Approved"]["Loan Amount"]
        denied_amounts = filtered_df[filtered_df["Status"] == "Denied"]["Loan Amount"]
        ax2.bar(["Approved", "Denied"], [approved_amounts.sum(), denied_amounts.sum()], color=["#4CAF50", "#FF5722"])
        ax2.set_ylabel("Total Loan Amount ($)")
        ax2.set_title("Loan Amounts by Outcome")
        plt.tight_layout()
        st.pyplot(fig)

        # Credit Score vs. Loan Amount
        st.write("### Credit Score vs. Loan Amount")
        fig2, ax = plt.subplots()
        filtered_df.plot(kind="scatter", x="Credit Score", y="Loan Amount", c="Status", colormap="viridis", ax=ax)
        ax.set_title("Credit Score vs. Loan Amount")
        st.pyplot(fig2)
    else:
        st.write("No data for analysis. Submit a loan request first.")

# Sidebar Info
st.sidebar.write("**Sample Request:**")
st.sidebar.write("- ID: USER001, Name: Jane Doe, Income: $4,000, Debt: $800, Score: 650, Loan: $10,000, Term: 3 yrs")
if st.sidebar.button("Reset Data"):
    st.session_state.loan_applications = []
    st.sidebar.success("All data reset!")

# Footer
st.write("Built with Streamlit by Nathan Rossow at (Burst Software)")
