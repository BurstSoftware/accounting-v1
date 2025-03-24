import streamlit as st

# Set page configuration
st.set_page_config(page_title="Accounting Basics & Principles", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a Topic",
    [
        "Home",
        "Key Concepts",
        "Double-Entry System",
        "Financial Statements",
        "Bookkeeping vs. Accounting",
        "Basic Methods",
        "Common Terms",
        "Principle of Regularity",
        "Principle of Consistency",
        "Principle of Sincerity",
        "Principle of Permanence of Methods",
        "Principle of Non-Compensation",
        "Principle of Prudence",
        "Principle of Continuity",
        "Principle of Periodicity",
        "Principle of Full Disclosure",
        "Principle of Materiality",
        "Principle of Utmost Good Faith",
        "Principle of Conservatism",
        "Principle of Objectivity",
        "Principle of Matching",
        "Principle of Revenue Recognition",
        "Principle of Historical Cost",
        "Principle of Monetary Unit",
        "Principle of Going Concern",
        "Principle of Substance Over Form",
        "Principle of Comparability",
        "Principle of Relevance",
        "Principle of Simplicity"
    ]
)

# Page content
if page == "Home":
    st.title("Accounting Basics & Principles")
    st.write("""
    Welcome to this interactive guide on accounting! Use the sidebar to explore fundamental accounting concepts and principles.
    Each page provides an explanation of a key topic to help you understand how accounting works and why it matters.
    """)

# Accounting Basics
elif page == "Key Concepts":
    st.title("Key Concepts")
    st.write("""
    - **Assets**: Things a business owns (e.g., cash, equipment, inventory).
    - **Liabilities**: What a business owes (e.g., loans, bills).
    - **Equity**: The owner’s stake in the business (Assets - Liabilities).
    - **Revenue**: Money earned from selling goods or services.
    - **Expenses**: Costs incurred to run the business (e.g., rent, salaries).
    - **Accounting Equation**: Assets = Liabilities + Equity.
    """)

elif page == "Double-Entry System":
    st.title("Double-Entry System")
    st.write("""
    - Every transaction affects at least two accounts (e.g., spending cash to buy equipment reduces cash and increases equipment).
    - Keeps the accounting equation balanced.
    - **Debits and Credits**: Debits increase assets/expenses and decrease liabilities/equity/revenue; credits do the opposite.
    """)

elif page == "Financial Statements":
    st.title("Financial Statements")
    st.write("""
    - **Balance Sheet**: Snapshot of assets, liabilities, and equity at a specific time.
    - **Income Statement**: Shows revenue, expenses, and profit/loss over a period.
    - **Cash Flow Statement**: Tracks cash inflows and outflows (operations, investing, financing).
    """)

elif page == "Bookkeeping vs. Accounting":
    st.title("Bookkeeping vs. Accounting")
    st.write("""
    - **Bookkeeping**: Recording daily transactions (e.g., sales, purchases).
    - **Accounting**: Interpreting and summarizing data for reports and decisions.
    """)

elif page == "Basic Methods":
    st.title("Basic Methods")
    st.write("""
    - **Accrual Basis**: Record revenue/expenses when earned/incurred, not when cash changes hands.
    - **Cash Basis**: Record revenue/expenses only when cash is received or paid.
    """)

elif page == "Common Terms":
    st.title("Common Terms")
    st.write("""
    - **Ledger**: System where transactions are recorded.
    - **Journal**: Where transactions are first entered chronologically.
    - **Trial Balance**: A check to ensure debits equal credits.
    """)

# Accounting Principles
elif page == "Principle of Regularity":
    st.title("Principle of Regularity")
    st.write("Accountants adhere to consistent rules and standards (e.g., GAAP or IFRS) in all financial reporting.")

elif page == "Principle of Consistency":
    st.title("Principle of Consistency")
    st.write("Accounting methods should remain consistent over time for comparability; changes must be disclosed.")

elif page == "Principle of Sincerity":
    st.title("Principle of Sincerity")
    st.write("Accountants provide an honest, impartial, and accurate representation of financials.")

elif page == "Principle of Permanence of Methods":
    st.title("Principle of Permanence of Methods")
    st.write("Use the same techniques consistently to ensure comparability.")

elif page == "Principle of Non-Compensation":
    st.title("Principle of Non-Compensation")
    st.write("Don’t offset debts with assets or expenses with revenue—report each separately.")

elif page == "Principle of Prudence":
    st.title("Principle of Prudence")
    st.write("Base reporting on factual, conservative estimates, avoiding speculation.")

elif page == "Principle of Continuity":
    st.title("Principle of Continuity")
    st.write("Assume the business will continue operating, affecting asset/liability valuation.")

elif page == "Principle of Periodicity":
    st.title("Principle of Periodicity")
    st.write("Divide financial reporting into standard time periods (e.g., quarters, years).")

elif page == "Principle of Full Disclosure":
    st.title("Principle of Full Disclosure")
    st.write("Disclose all relevant financial information, including risks, in reports or notes.")

elif page == "Principle of Materiality":
    st.title("Principle of Materiality")
    st.write("Focus on significant items that influence decisions; minor errors can be overlooked if immaterial.")

elif page == "Principle of Utmost Good Faith":
    st.title("Principle of Utmost Good Faith")
    st.write("All parties act honestly and ethically in financial reporting.")

elif page == "Principle of Conservatism":
    st.title("Principle of Conservatism")
    st.write("Choose options that understate rather than overstate financial health in uncertainty.")

elif page == "Principle of Objectivity":
    st.title("Principle of Objectivity")
    st.write("Base reporting on verifiable evidence (e.g., invoices), not opinions.")

elif page == "Principle of Matching":
    st.title("Principle of Matching")
    st.write("Record expenses in the same period as the revenues they generate.")

elif page == "Principle of Revenue Recognition":
    st.title("Principle of Revenue Recognition")
    st.write("Record revenue when earned (goods/services delivered), not necessarily when paid.")

elif page == "Principle of Historical Cost":
    st.title("Principle of Historical Cost")
    st.write("Record assets/liabilities at their original cost, not current market value.")

elif page == "Principle of Monetary Unit":
    st.title("Principle of Monetary Unit")
    st.write("Record transactions in a stable currency; only monetary items are included.")

elif page == "Principle of Going Concern":
    st.title("Principle of Going Concern")
    st.write("Assume the business will operate indefinitely unless evidence suggests otherwise.")

elif page == "Principle of Substance Over Form":
    st.title("Principle of Substance Over Form")
    st.write("Reflect the economic reality of transactions over their legal form.")

elif page == "Principle of Comparability":
    st.title("Principle of Comparability")
    st.write("Prepare statements for comparison across periods or companies with consistent standards.")

elif page == "Principle of Relevance":
    st.title("Principle of Relevance")
    st.write("Provide useful, pertinent information for decision-makers, balancing timeliness and accuracy.")

elif page == "Principle of Simplicity":
    st.title("Principle of Simplicity")
    st.write("Keep accounting straightforward while meeting reporting needs.")

# Footer
st.sidebar.write("Built with Streamlit by Grok 3 (xAI)")
