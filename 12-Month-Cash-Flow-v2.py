import streamlit as st
import pandas as pd

def create_cash_flow_app():
    st.title('12 Month Cash Flow Spreadsheet')
    
    # Company Details
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input('Enter Company Name')
    with col2:
        fiscal_year = st.text_input('Fiscal Year Begins', 'Jan-YY')

    # Create monthly columns
    months = ['Pre-Startup EST'] + [f'{m}-YY' for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    
    # Initialize session state for storing values
    if 'cash_flow_data' not in st.session_state:
        st.session_state.cash_flow_data = {
            'Cash on Hand': [0] * 14,
            'CASH RECEIPTS': [],
            'Cash Sales': [0] * 14,
            'Collections fm CR accounts': [0] * 14,
            'Loan/ other cash in': [0] * 14,
            'TOTAL CASH RECEIPTS': [0] * 14,
            'Total Cash Available': [0] * 14,
            'CASH PAID OUT': [],
            'Purchases (merchandise)': [0] * 14,
            'Purchases (specify)': [0] * 14,
            'Gross wages': [0] * 14,
            'Payroll expenses': [0] * 14,
            'Outside services': [0] * 14,
            'Supplies': [0] * 14,
            'Repairs & maintenance': [0] * 14,
            'Advertising': [0] * 14,
            'Car, delivery & travel': [0] * 14,
            'Accounting & legal': [0] * 14,
            'Rent': [0] * 14,
            'Telephone': [0] * 14,
            'Utilities': [0] * 14,
            'Insurance': [0] * 14,
            'Taxes': [0] * 14,
            'Interest': [0] * 14,
            'Other expenses': [0] * 14,
            'Miscellaneous': [0] * 14,
            'SUBTOTAL': [0] * 14,
            'Loan principal payment': [0] * 14,
            'Capital purchases': [0] * 14,
            'Other startup costs': [0] * 14,
            'Reserve and/or Escrow': [0] * 14,
            'Owners\' Withdrawal': [0] * 14,
            'TOTAL CASH PAID OUT': [0] * 14,
            'Cash Position': [0] * 14,
            'ESSENTIAL OPERATING DATA': [],
            'Sales Volume': [0] * 14,
            'Accounts Receivable': [0] * 14,
            'Bad Debt': [0] * 14,
            'Inventory on hand': [0] * 14,
            'Accounts Payable': [0] * 14,
            'Depreciation': [0] * 14
        }

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(['Cash Receipts', 'Cash Paid Out', 'Operating Data'])

    def check_and_extend_list(item, expected_length=14):
        # Ensures the list for each item has the correct length
        current_length = len(st.session_state.cash_flow_data[item])
        if current_length < expected_length:
            st.session_state.cash_flow_data[item].extend([0] * (expected_length - current_length))
        elif current_length > expected_length:
            st.session_state.cash_flow_data[item] = st.session_state.cash_flow_data[item][:expected_length]
        return st.session_state.cash_flow_data[item]

    with tab1:
        st.subheader('Cash Receipts')
        receipt_items = ['Cash Sales', 'Collections fm CR accounts', 'Loan/ other cash in']
        for item in receipt_items:
            st.text(item)
            check_and_extend_list(item)  # Ensure the list for each item has the correct length
            cols = st.columns(14)
            for i, col in enumerate(cols):
                with col:
                    key = f'{item}_{i}'
                    value = st.number_input(months[i], key=key, value=st.session_state.cash_flow_data[item][i])
                    st.session_state.cash_flow_data[item][i] = value

    with tab2:
        st.subheader('Cash Paid Out')
        expense_items = ['Purchases (merchandise)', 'Purchases (specify)', 'Gross wages', 'Payroll expenses',
                        'Outside services', 'Supplies', 'Repairs & maintenance', 'Advertising',
                        'Car, delivery & travel', 'Accounting & legal', 'Rent', 'Telephone',
                        'Utilities', 'Insurance', 'Taxes', 'Interest', 'Other expenses',
                        'Miscellaneous', 'Loan principal payment', 'Capital purchases',
                        'Other startup costs', 'Reserve and/or Escrow', 'Owners\' Withdrawal']
        
        for item in expense_items:
            st.text(item)
            check_and_extend_list(item)  # Ensure the list for each item has the correct length
            cols = st.columns(14)
            for i, col in enumerate(cols):
                with col:
                    key = f'{item}_{i}'
                    value = st.number_input(months[i], key=key, value=st.session_state.cash_flow_data[item][i])
                    st.session_state.cash_flow_data[item][i] = value

    with tab3:
        st.subheader('Essential Operating Data')
        operating_items = ['Sales Volume', 'Accounts Receivable', 'Bad Debt',
                          'Inventory on hand', 'Accounts Payable', 'Depreciation']
        
        for item in operating_items:
            st.text(item)
            check_and_extend_list(item)  # Ensure the list for each item has the correct length
            cols = st.columns(14)
            for i, col in enumerate(cols):
                with col:
                    key = f'{item}_{i}'
                    value = st.number_input(months[i], key=key, value=st.session_state.cash_flow_data[item][i])
                    st.session_state.cash_flow_data[item][i] = value

    # Calculate totals
    for i in range(14):
        # Calculate TOTAL CASH RECEIPTS
        st.session_state.cash_flow_data['TOTAL CASH RECEIPTS'][i] = (
            st.session_state.cash_flow_data['Cash Sales'][i] +
            st.session_state.cash_flow_data['Collections fm CR accounts'][i] +
            st.session_state.cash_flow_data['Loan/ other cash in'][i]
        )
        
        # Calculate Total Cash Available
        if i == 0:
            st.session_state.cash_flow_data['Total Cash Available'][i] = (
                st.session_state.cash_flow_data['Cash on Hand'][i] +
                st.session_state.cash_flow_data['TOTAL CASH RECEIPTS'][i]
            )
        else:
            st.session_state.cash_flow_data['Total Cash Available'][i] = (
                st.session_state.cash_flow_data['Cash Position'][i-1] +
                st.session_state.cash_flow_data['TOTAL CASH RECEIPTS'][i]
            )

        # Calculate SUBTOTAL of expenses
        subtotal = sum(st.session_state.cash_flow_data[item][i] for item in expense_items)
        st.session_state.cash_flow_data['SUBTOTAL'][i] = subtotal
        
        # Calculate TOTAL CASH PAID OUT
        st.session_state.cash_flow_data['TOTAL CASH PAID OUT'][i] = subtotal
        
        # Calculate Cash Position
        st.session_state.cash_flow_data['Cash Position'][i] = (
            st.session_state.cash_flow_data['Total Cash Available'][i] -
            st.session_state.cash_flow_data['TOTAL CASH PAID OUT'][i]
        )

    # Export to CSV
    if st.button('Export to CSV'):
        df = pd.DataFrame(st.session_state.cash_flow_data, index=months)
        csv = df.to_csv(index=True)
        
        # Create a download button
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='cash_flow.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    create_cash_flow_app()
