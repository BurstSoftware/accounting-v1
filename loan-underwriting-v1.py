import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Loan Underwriting", layout="wide")

# Title and Introduction
st.title("Loan Underwriting")
st.write("""
Loan underwriting assesses an applicant’s creditworthiness for loans such as:
- **Housing Loans (Mortgages)**: Long-term loans for property purchase.
- **Car Loans**: Medium-term loans for vehicle purchase.
- **Additional Loans**: Personal loans for various purposes.
""")
st.write("""
This app evaluates applications based on income, debt, credit score, and collateral, then generates accounting entries for approved loans.
Key metrics include:
- **Debt-to-Income (DTI) Ratio**: Monthly debt payments / Monthly income.
- **Loan-to-Value (LTV) Ratio**: Loan amount / Asset value.
- **Credit Score**: Indicator of repayment history.
""")

# Initialize Session State
if "applications" not in st.session_state:
    st.session_state.applications = []

# Sidebar Navigation
st.sidebar.title("Underwriting Tools")
option = st.sidebar.selectbox(
    "Choose a Task",
    ["Submit Application", "Review Applications", "Underwriting Decision", "Accounting Entries", "Analysis & Visualization"]
)
evaluation_date = st.sidebar.date_input("Evaluation Date", value=datetime(2025, 3, 23))

# --- Submit Application ---
if option == "Submit Application":
    st.subheader("Submit Loan Application")
    st.write("Enter applicant details for underwriting.")

    with st.form(key="application_form"):
        # Applicant Info
        applicant_id = st.text_input("Applicant ID", "e.g., APP001")
        name = st.text_input("Applicant Name")
        loan_type = st.selectbox("Loan Type", ["Housing Loan", "Car Loan", "Additional Loan"])

        # Financial Info
        monthly_income = st.number_input("Monthly Income ($)", min_value=0.0, value=5000.0)
        existing_debt_payments = st.number_input("Existing Monthly Debt Payments ($)", min_value=0.0, value=1000.0)
        credit_score = st.number_input("Credit Score (300-850)", min_value=300, max_value=850, value=700)

        # Loan Details
        loan_amount = st.number_input("Requested Loan Amount ($)", min_value=0.0, value=200000.0 if loan_type == "Housing Loan" else 20000.0)
        term_years = st.number_input("Loan Term (Years)", min_value=1, value=30 if loan_type == "Housing Loan" else 5)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, value=4.0 if loan_type == "Housing Loan" else 6.0, step=0.1)

        # Collateral (if applicable)
        asset_value = st.number_input("Asset Value ($)", min_value=0.0, value=250000.0 if loan_type == "Housing Loan" else 25000.0 if loan_type == "Car Loan" else 0.0, 
                                      disabled=loan_type == "Additional Loan")

        submit_button = st.form_submit_button(label="Submit Application")

    if submit_button:
        if not applicant_id or not name:
            st.error("Applicant ID and Name are required!")
        else:
            monthly_payment = (loan_amount * (interest_rate / 1200)) / (1 - (1 + interest_rate / 1200) ** (-term_years * 12))
            application = {
                "Applicant ID": applicant_id,
                "Name": name,
                "Loan Type": loan_type,
                "Monthly Income": monthly_income,
                "Existing Debt Payments": existing_debt_payments,
                "Credit Score": credit_score,
                "Loan Amount": loan_amount,
                "Term (Years)": term_years,
                "Interest Rate": interest_rate / 100,
                "Monthly Payment": monthly_payment,
                "Asset Value": asset_value,
                "Date Submitted": evaluation_date,
                "Status": "Pending"
            }
            st.session_state.applications.append(application)
            st.success(f"Application submitted for {name} - {loan_type}")

    # Display Submitted Applications
    if st.session_state.applications:
        st.write("### Submitted Applications")
        apps_df = pd.DataFrame(st.session_state.applications)
        st.dataframe(apps_df)

# --- Review Applications ---
elif option == "Review Applications":
    st.subheader("Review Applications")
    st.write("View all submitted loan applications.")

    if st.session_state.applications:
        apps_df = pd.DataFrame(st.session_state.applications)
        filtered_df = apps_df[apps_df["Date Submitted"] == evaluation_date]
        st.dataframe(filtered_df)
    else:
        st.write("No applications submitted yet.")

# --- Underwriting Decision ---
elif option == "Underwriting Decision":
    st.subheader("Underwriting Decision")
    st.write("Evaluate and decide on loan applications.")

    if not st.session_state.applications:
        st.warning("No applications to evaluate.")
    else:
        apps_df = pd.DataFrame(st.session_state.applications)
        pending_df = apps_df[apps_df["Status"] == "Pending"]

        if pending_df.empty:
            st.write("No pending applications.")
        else:
            selected_app = st.selectbox(
                "Select Application",
                pending_df.index,
                format_func=lambda x: f"{pending_df.loc[x, 'Name']} - {pending_df.loc[x, 'Loan Type']} (${pending_df.loc[x, 'Loan Amount']:.2f})"
            )
            app = pending_df.loc[selected_app]

            # Calculate Metrics
            total_debt_payments = app["Existing Debt Payments"] + app["Monthly Payment"]
            dti_ratio = (total_debt_payments / app["Monthly Income"]) * 100 if app["Monthly Income"] > 0 else 100
            ltv_ratio = (app["Loan Amount"] / app["Asset Value"]) * 100 if app["Asset Value"] > 0 else 0

            st.write("### Applicant Details")
            st.write(f"**Name**: {app['Name']}")
            st.write(f"**Loan Type**: {app['Loan Type']}")
            st.write(f"**Loan Amount**: ${app['Loan Amount']:.2f}")
            st.write(f"**Monthly Payment**: ${app['Monthly Payment']:.2f}")
            st.write(f"**Credit Score**: {app['Credit Score']}")
            st.write(f"**DTI Ratio**: {dti_ratio:.2f}%")
            if app["Asset Value"] > 0:
                st.write(f"**LTV Ratio**: {ltv_ratio:.2f}%")

            # Decision Criteria (Simplified)
            dti_threshold = 43.0  # Common max DTI for mortgages
            ltv_threshold = 80.0  # Common max LTV for secured loans
            credit_threshold = 620  # Minimum credit score

            st.write("### Evaluation")
            issues = []
            if dti_ratio > dti_threshold:
                issues.append(f"DTI Ratio ({dti_ratio:.2f}%) exceeds threshold ({dti_threshold}%)")
            if ltv_ratio > ltv_threshold and app["Asset Value"] > 0:
                issues.append(f"LTV Ratio ({ltv_ratio:.2f}%) exceeds threshold ({ltv_threshold}%)")
            if app["Credit Score"] < credit_threshold:
                issues.append(f"Credit Score ({app['Credit Score']}) below threshold ({credit_threshold})")

            if not issues:
                st.success("No major issues detected.")
            else:
                for issue in issues:
                    st.warning(issue)

            # Decision
            decision = st.radio("Decision", ["Approve", "Deny"], index=0 if not issues else 1)
            if st.button("Submit Decision"):
                st.session_state.applications[selected_app]["Status"] = decision
                st.success(f"Application {decision}d for {app['Name']} - {app['Loan Type']}")

# --- Accounting Entries ---
elif option == "Accounting Entries":
    st.subheader("Accounting Entries")
    st.write("Generate double-entry journal entries for approved loans.")

    if st.session_state.applications:
        apps_df = pd.DataFrame(st.session_state.applications)
        approved_df = apps_df[apps_df["Status"] == "Approve"]

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
    st.write("Analyze underwriting data.")

    if st.session_state.applications:
        apps_df = pd.DataFrame(st.session_state.applications)
        filtered_df = apps_df[apps_df["Date Submitted"] == evaluation_date]

        # Summary
        st.write("### Application Summary")
        summary = {
            "Total Applications": len(filtered_df),
            "Approved": len(filtered_df[filtered_df["Status"] == "Approve"]),
            "Denied": len(filtered_df[filtered_df["Status"] == "Deny"]),
            "Pending": len(filtered_df[filtered_df["Status"] == "Pending"]),
            "Total Loan Amount (Approved)": filtered_df[filtered_df["Status"] == "Approve"]["Loan Amount"].sum()
        }
        summary_df = pd.DataFrame.from_dict(summary, orient="index", columns=["Value"])
        st.table(summary_df)

        # Visualization
        st.write("### Loan Distribution")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Pie Chart: Status
        status_counts = filtered_df["Status"].value_counts()
        ax1.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
        ax1.set_title("Application Status")
        ax1.axis("equal")

        # Bar Chart: Loan Type
        type_totals = filtered_df.groupby("Loan Type")["Loan Amount"].sum()
        ax2.bar(type_totals.index, type_totals, color=["#4CAF50", "#FF5722", "#2196F3"])
        ax2.set_ylabel("Total Loan Amount ($)")
        ax2.set_title("Loan Amount by Type")
        plt.tight_layout()
        st.pyplot(fig)

        # Credit Score Distribution
        st.write("### Credit Score Distribution")
        fig2, ax = plt.subplots()
        filtered_df["Credit Score"].hist(bins=10, ax=ax, color="#2196F3")
        ax.set_xlabel("Credit Score")
        ax.set_ylabel("Number of Applicants")
        ax.set_title("Credit Score Histogram")
        st.pyplot(fig2)
    else:
        st.write("No data for analysis. Submit applications first.")

# Sidebar Info
st.sidebar.write("**Sample Application:**")
st.sidebar.write("- ID: APP001, Name: John Doe, Housing Loan, $200,000, 30 yrs, 4%, Income: $5,000, Debt: $1,000, Score: 700, Asset: $250,000")
if st.sidebar.button("Reset Data"):
    st.session_state.applications = []
    st.sidebar.success("All data reset!")

# Footer
st.write("Built with Streamlit by Grok 3 (xAI)")
