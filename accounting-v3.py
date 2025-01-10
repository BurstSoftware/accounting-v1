import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Account:
    def __init__(self, name, account_type, balance=0):
        self.name = name
        self.account_type = account_type  # e.g., "asset", "liability", "income", "expense"
        self.balance = balance

    def __repr__(self):
        return f"{self.name} ({self.account_type}): {self.balance:.2f}"


class AccountingApp:
    def __init__(self):
        self.accounts = {}

    def create_account(self, name, account_type, initial_balance=0):
        if name in self.accounts:
            st.warning(f"Account with name '{name}' already exists.")
            return
        self.accounts[name] = Account(name, account_type, initial_balance)
        st.success(f"Account '{name}' created successfully.")

    def record_transaction(self, debit_account, credit_account, amount):
        if debit_account not in self.accounts or credit_account not in self.accounts:
            st.error("One or both accounts do not exist.")
            return

        if amount <= 0:
            st.error("Transaction amount must be positive.")
            return

        self.accounts[debit_account].balance += amount
        self.accounts[credit_account].balance -= amount
        st.success(f"Transaction recorded: Debit {debit_account} / Credit {credit_account} - {amount:.2f}")

    def generate_balance_sheet(self):
        assets = [(acc.name, acc.balance) for acc in self.accounts.values() if acc.account_type == "asset"]
        liabilities = [(acc.name, acc.balance) for acc in self.accounts.values() if acc.account_type == "liability"]
        equity = sum(balance for _, balance in assets) - sum(balance for _, balance in liabilities)

        data = {
            "Assets": dict(assets),
            "Liabilities": dict(liabilities),
            "Equity": equity
        }

        df = pd.DataFrame({"Type": ["Asset", "Liability", "Equity"],
                           "Total": [sum(balance for _, balance in assets),
                                      sum(balance for _, balance in liabilities),
                                      equity]})
        return data, df

    def list_accounts(self):
        account_data = [(acc.name, acc.account_type, acc.balance) for acc in self.accounts.values()]
        return pd.DataFrame(account_data, columns=["Account Name", "Type", "Balance"])


def download_csv(df, filename):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label=f"Download {filename}.csv", data=csv, file_name=f"{filename}.csv", mime="text/csv")


def download_pdf(data, filename):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    y = 750
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(30, y, f"{filename}")
    y -= 30

    pdf.setFont("Helvetica", 12)
    for key, values in data.items():
        if isinstance(values, dict):
            pdf.drawString(30, y, f"{key}:")
            y -= 20
            for subkey, subvalue in values.items():
                pdf.drawString(50, y, f"- {subkey}: {subvalue:.2f}")
                y -= 20
        else:
            pdf.drawString(30, y, f"{key}: {values:.2f}")
            y -= 20

    pdf.save()
    buffer.seek(0)
    st.download_button(label=f"Download {filename}.pdf", data=buffer, file_name=f"{filename}.pdf", mime="application/pdf")


def get_app():
    if "app" not in st.session_state:
        st.session_state.app = AccountingApp()
    return st.session_state.app


def main():
    st.title("Accounting Application")
    app = get_app()

    menu = ["Create Account", "Record Transaction", "Generate Balance Sheet", "List Accounts"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create Account":
        st.subheader("Create Account")
        name = st.text_input("Enter account name")
        account_type = st.selectbox("Enter account type", ["asset", "liability", "income", "expense"])
        initial_balance = st.number_input("Enter initial balance", min_value=0.0, step=0.01)
        if st.button("Create Account"):
            app.create_account(name, account_type, initial_balance)

    elif choice == "Record Transaction":
        st.subheader("Record Transaction")
        account_names = list(app.accounts.keys())
        if account_names:
            debit_account = st.selectbox("Select debit account", account_names)
            credit_account = st.selectbox("Select credit account", account_names)
            amount = st.number_input("Enter transaction amount", min_value=0.0, step=0.01)
            if st.button("Record Transaction"):
                app.record_transaction(debit_account, credit_account, amount)
        else:
            st.warning("No accounts available. Please create accounts first.")

    elif choice == "Generate Balance Sheet":
        st.subheader("Generate Balance Sheet")
        data, df = app.generate_balance_sheet()
        st.dataframe(df)
        download_csv(df, "balance_sheet")
        download_pdf(data, "Balance_Sheet")

    elif choice == "List Accounts":
        st.subheader("List Accounts")
        df = app.list_accounts()
        st.dataframe(df)
        download_csv(df, "accounts")
        download_pdf(df.to_dict(orient='list'), "Accounts")


if __name__ == "__main__":
    main()
