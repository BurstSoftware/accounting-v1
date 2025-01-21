import streamlit as st
import pandas as pd

def create_cash_flow_app():
    st.title('12 Month Cash Flow Spreadsheet')
    
    # Add error handling banner
    if 'error_message' in st.session_state:
        st.error(st.session_state.error_message)
        del st.session_state.error_message

    # Company Details
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input('Enter Company Name')
    with col2:
        fiscal_year = st.text_input('Fiscal Year Begins', 'Jan-YY')

    # Create monthly columns
    months = ['Pre-Startup EST'] + [f'{m}-YY' for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    
    # Initialize session state for storing values with proper structure
    if 'cash_flow_data' not in st.session_state:
        st.session_state.cash_flow_data = {
            'Cash on Hand': [0] * 14,
            'CASH RECEIPTS': [0] * 14,  # Changed from empty list to initialized list
            'Cash Sales': [0] * 14,
            'Collections fm CR accounts': [0] * 14,
            'Loan/ other cash in': [0] * 14,
            'TOTAL CASH RECEIPTS': [0] * 14,
            'Total Cash Available': [0] * 14,
            'CASH PAID OUT': [0] * 14,  # Changed from empty list to initialized list
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
            'ESSENTIAL OPERATING DATA': [0] * 14,  # Changed from empty list to initialized list
            'Sales Volume': [0] * 14,
            'Accounts Receivable': [0] * 14,
            'Bad Debt': [0] * 14,
            'Inventory on hand': [0] * 14,
            'Accounts Payable': [0] * 14,
            'Depreciation': [0] * 14
        }

    def validate_data_length(item):
        """Validates and fixes the length of data lists"""
        try:
            if len(st.session_state.cash_flow_data[item]) != 14:
                st.session_state.cash_flow_data[item] = [0] * 14
                st.warning(f"Reset {item} data due to invalid length")
        except Exception as e:
            st.session_state.cash_flow_data[item] = [0] * 14
            st.error(f"Error processing {item}: {str(e)}")

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(['Cash Receipts', 'Cash Paid Out', 'Operating Data'])

    with tab1:
        st.subheader('Cash Receipts')
        receipt_items = ['Cash Sales', 'Collections fm CR accounts', 'Loan/ other cash in']
        for item in receipt_items:
            validate_data_length(item)
            st.text(item)
            cols = st.columns(14)
            for i, col in enumerate(cols):
                with col:
                    try:
                        key = f'{item}_{i}'
                        value = st.number_input(
                            months[i], 
                            key=key,
                            value=float(st.session_state.cash_flow_data[item][i]),
                            step=0.01
                        )
                        st.session_state.cash_flow_data[item][i] = value
                    except Exception as e:
                        st.error(f"Error in {item} at month {i}")
                        st.session_state.cash_flow_data[item][i] = 0

    with tab2:
        st.subheader('Cash Paid Out')
        expense_items = ['Purchases (merchandise)', 'Purchases (specify)', 'Gross wages', 'Payroll expenses',
                        'Outside services', 'Supplies', 'Repairs & maintenance', 'Advertising',
                        'Car, delivery & travel', 'Accounting & legal', 'Rent', 'Telephone',
                        'Utilities', 'Insurance', 'Taxes', 'Interest', 'Other expenses',
                        'Miscellaneous', 'Loan principal payment', 'Capital purchases',
                        'Other startup costs', 'Reserve and/or Escrow', 'Owners\' Withdrawal']
        
        for item in expense_items:
            validate_data_length(item)
            st.text(item)
            cols = st.columns(14)
            for i, col in enumerate(cols):
                with col:
                    try:
                        key = f'{item}_{i}'
                        value = st.number_input(
                            months[i],
                            key=key,
                            value=float(st.session_state.cash_flow_data[item][i]),
                            step=0.01
                        )
                        st.session_state.cash_flow_data[item][i] = value
                    except Exception as e:
                        st.error(f"Error in {item} at month {i}")
                        st.session_state.cash_flow_data[item][i] = 0

    with tab3:
        st.subheader('Essential Operating Data')
        operating_items = ['Sales Volume', 'Accounts Receivable', 'Bad Debt',
                          'Inventory on hand', 'Accounts Payable', 'Depreciation']
        
        for item in operating_items:
            validate_data_length(item)
            st.text(item)
            cols = st.columns(14)
            for i, col in enumerate(cols):
                with col:
                    try:
                        key = f'{item}_{i}'
                        value = st.number_input(
                            months[i],
                            key=key,
                            value=float(st.session_state.cash_flow_data[item][i]),
                            step=0.01
                        )
                        st.session_state.cash_flow_data[item][i] = value
                    except Exception as e:
                        st.error(f"Error in {item} at month {i}")
                        st.session_state.cash_flow_data[item][i] = 0

    try:
        # Calculate totals
        for i in range(14):
            # Calculate TOTAL CASH RECEIPTS
            total_receipts = sum(st.session_state.cash_flow_data[item][i] for item in receipt_items)
            st.session_state.cash_flow_data['TOTAL CASH RECEIPTS'][i] = total_receipts
            
            # Calculate Total Cash Available
            if i == 0:
                cash_available = (st.session_state.cash_flow_data['Cash on Hand'][i] + total_receipts)
            else:
                cash_available = (st.session_state.cash_flow_data['Cash Position'][i-1] + total_receipts)
            st.session_state.cash_flow_data['Total Cash Available'][i] = cash_available

            # Calculate SUBTOTAL of expenses
            subtotal = sum(st.session_state.cash_flow_data[item][i] for item in expense_items)
            st.session_state.cash_flow_data['SUBTOTAL'][i] = subtotal
            
            # Calculate TOTAL CASH PAID OUT
            st.session_state.cash_flow_data['TOTAL CASH PAID OUT'][i] = subtotal
            
            # Calculate Cash Position
            st.session_state.cash_flow_data['Cash Position'][i] = cash_available - subtotal
    except Exception as e:
        st.error(f"Error calculating totals: {str(e)}")

    # Display totals
    st.subheader("Monthly Totals")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Cash Receipts", f"${st.session_state.cash_flow_data['TOTAL CASH RECEIPTS'][-1]:,.2f}")
    with col2:
        st.metric("Total Cash Paid Out", f"${st.session_state.cash_flow_data['TOTAL CASH PAID OUT'][-1]:,.2f}")
    with col3:
        st.metric("Cash Position", f"${st.session_state.cash_flow_data['Cash Position'][-1]:,.2f}")

    # Export to CSV
    if st.button('Export to CSV'):
        try:
            df = pd.DataFrame(st.session_state.cash_flow_data, index=months)
            csv = df.to_csv(index=True)
            
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='cash_flow.csv',
                mime='text/csv'
            )
        except Exception as e:
            st.error(f"Error exporting to CSV: {str(e)}")

if __name__ == '__main__':
    create_cash_flow_app()
