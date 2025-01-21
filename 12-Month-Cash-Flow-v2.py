import streamlit as st
import pandas as pd

def display_month_data(month_index, month_name, cash_flow_data):
    st.header(f"{month_name} Cash Flow Data")
    
    # Create three columns for different sections
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Cash Receipts")
        receipt_items = ['Cash on Hand', 'Cash Sales', 'Collections fm CR accounts', 'Loan/ other cash in']
        for item in receipt_items:
            try:
                value = st.number_input(
                    f"{item}",
                    value=float(cash_flow_data[item][month_index]),
                    step=0.01,
                    key=f"{item}_{month_index}"
                )
                cash_flow_data[item][month_index] = value
            except Exception as e:
                st.error(f"Error in {item}")
                cash_flow_data[item][month_index] = 0
                
        # Display total receipts
        total_receipts = cash_flow_data['TOTAL CASH RECEIPTS'][month_index]
        st.metric("Total Cash Receipts", f"${total_receipts:,.2f}")

    with col2:
        st.subheader("Cash Paid Out")
        expense_items = ['Purchases (merchandise)', 'Purchases (specify)', 'Gross wages', 'Payroll expenses',
                        'Outside services', 'Supplies', 'Repairs & maintenance', 'Advertising',
                        'Car, delivery & travel', 'Accounting & legal', 'Rent', 'Telephone',
                        'Utilities', 'Insurance', 'Taxes', 'Interest', 'Other expenses',
                        'Miscellaneous', 'Loan principal payment', 'Capital purchases',
                        'Other startup costs', 'Reserve and/or Escrow', 'Owners\' Withdrawal']
        
        for item in expense_items:
            try:
                value = st.number_input(
                    f"{item}",
                    value=float(cash_flow_data[item][month_index]),
                    step=0.01,
                    key=f"{item}_{month_index}"
                )
                cash_flow_data[item][month_index] = value
            except Exception as e:
                st.error(f"Error in {item}")
                cash_flow_data[item][month_index] = 0
                
        # Display total paid out
        total_paid = cash_flow_data['TOTAL CASH PAID OUT'][month_index]
        st.metric("Total Cash Paid Out", f"${total_paid:,.2f}")

    with col3:
        st.subheader("Operating Data")
        operating_items = ['Sales Volume', 'Accounts Receivable', 'Bad Debt',
                          'Inventory on hand', 'Accounts Payable', 'Depreciation']
        
        for item in operating_items:
            try:
                value = st.number_input(
                    f"{item}",
                    value=float(cash_flow_data[item][month_index]),
                    step=0.01,
                    key=f"{item}_{month_index}"
                )
                cash_flow_data[item][month_index] = value
            except Exception as e:
                st.error(f"Error in {item}")
                cash_flow_data[item][month_index] = 0

        # Display cash position
        cash_position = cash_flow_data['Cash Position'][month_index]
        st.metric("Cash Position", f"${cash_position:,.2f}")

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
    
    # Initialize session state
    if 'cash_flow_data' not in st.session_state:
        st.session_state.cash_flow_data = {
            'Cash on Hand': [0] * 13,
            'CASH RECEIPTS': [0] * 13,
            'Cash Sales': [0] * 13,
            'Collections fm CR accounts': [0] * 13,
            'Loan/ other cash in': [0] * 13,
            'TOTAL CASH RECEIPTS': [0] * 13,
            'Total Cash Available': [0] * 13,
            'CASH PAID OUT': [0] * 13,
            'Purchases (merchandise)': [0] * 13,
            'Purchases (specify)': [0] * 13,
            'Gross wages': [0] * 13,
            'Payroll expenses': [0] * 13,
            'Outside services': [0] * 13,
            'Supplies': [0] * 13,
            'Repairs & maintenance': [0] * 13,
            'Advertising': [0] * 13,
            'Car, delivery & travel': [0] * 13,
            'Accounting & legal': [0] * 13,
            'Rent': [0] * 13,
            'Telephone': [0] * 13,
            'Utilities': [0] * 13,
            'Insurance': [0] * 13,
            'Taxes': [0] * 13,
            'Interest': [0] * 13,
            'Other expenses': [0] * 13,
            'Miscellaneous': [0] * 13,
            'SUBTOTAL': [0] * 13,
            'Loan principal payment': [0] * 13,
            'Capital purchases': [0] * 13,
            'Other startup costs': [0] * 13,
            'Reserve and/or Escrow': [0] * 13,
            'Owners\' Withdrawal': [0] * 13,
            'TOTAL CASH PAID OUT': [0] * 13,
            'Cash Position': [0] * 13,
            'ESSENTIAL OPERATING DATA': [0] * 13,
            'Sales Volume': [0] * 13,
            'Accounts Receivable': [0] * 13,
            'Bad Debt': [0] * 13,
            'Inventory on hand': [0] * 13,
            'Accounts Payable': [0] * 13,
            'Depreciation': [0] * 13
        }
    
    # Add page navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Month", months)
    month_index = months.index(page)
    
    # Display the selected month's data
    display_month_data(month_index, page, st.session_state.cash_flow_data)
    
    # Calculate totals after any changes
    try:
        for i in range(13):
            receipt_items = ['Cash Sales', 'Collections fm CR accounts', 'Loan/ other cash in']
            expense_items = ['Purchases (merchandise)', 'Purchases (specify)', 'Gross wages', 'Payroll expenses',
                           'Outside services', 'Supplies', 'Repairs & maintenance', 'Advertising',
                           'Car, delivery & travel', 'Accounting & legal', 'Rent', 'Telephone',
                           'Utilities', 'Insurance', 'Taxes', 'Interest', 'Other expenses',
                           'Miscellaneous', 'Loan principal payment', 'Capital purchases',
                           'Other startup costs', 'Reserve and/or Escrow', 'Owners\' Withdrawal']
            
            # Calculate TOTAL CASH RECEIPTS
            total_receipts = sum(st.session_state.cash_flow_data[item][i] for item in receipt_items)
            st.session_state.cash_flow_data['TOTAL CASH RECEIPTS'][i] = total_receipts
            
            # Calculate Total Cash Available
            if i == 0:
                cash_available = (st.session_state.cash_flow_data['Cash on Hand'][i] + total_receipts)
            else:
                cash_available = (st.session_state.cash_flow_data['Cash Position'][i-1] + total_receipts)
            st.session_state.cash_flow_data['Total Cash Available'][i] = cash_available
            
            # Calculate SUBTOTAL and TOTAL CASH PAID OUT
            subtotal = sum(st.session_state.cash_flow_data[item][i] for item in expense_items)
            st.session_state.cash_flow_data['SUBTOTAL'][i] = subtotal
            st.session_state.cash_flow_data['TOTAL CASH PAID OUT'][i] = subtotal
            
            # Calculate Cash Position
            st.session_state.cash_flow_data['Cash Position'][i] = cash_available - subtotal
    except Exception as e:
        st.error(f"Error calculating totals: {str(e)}")

    # Add summary view toggle
    if st.sidebar.checkbox("Show Summary View"):
        st.header("Summary View")
        df = pd.DataFrame(st.session_state.cash_flow_data, index=months)
        st.dataframe(df)

    # Export to CSV
    if st.sidebar.button('Export to CSV'):
        try:
            df = pd.DataFrame(st.session_state.cash_flow_data, index=months)
            csv = df.to_csv(index=True)
            
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name='cash_flow.csv',
                mime='text/csv'
            )
        except Exception as e:
            st.error(f"Error exporting to CSV: {str(e)}")

if __name__ == '__main__':
    create_cash_flow_app()
