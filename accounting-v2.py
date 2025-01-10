import streamlit as st

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
        st.header("Balance Sheet")
        total_assets = sum(acc.balance for acc in self.accounts.values() if acc.account_type == "asset")
        total_liabilities = sum(acc.balance for acc in self.accounts.values() if acc.account_type == "liability")
        equity = total_assets - total_liabilities

        st.subheader("Assets")
        for acc in self.accounts.values():
            if acc.account_type == "asset":
                st.write(f"  {acc.name}: {acc.balance:.2f}")

        st.subheader("Liabilities")
        for acc in self.accounts.values():
            if acc.account_type == "liability":
                st.write(f"  {acc.name}: {acc.balance:.2f}")

        st.subheader("Equity")
        st.write(f"  Total Equity: {equity:.2f}")

    def list_accounts(self):
        st.header("Accounts")
        for account in self.accounts.values():
            st.write(account)


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
        app.generate_balance_sheet()

    elif choice == "List Accounts":
        st.subheader("List Accounts")
        app.list_accounts()


if __name__ == "__main__":
    main()
