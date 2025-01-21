import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

# Set page configuration
st.set_page_config(
    page_title="12-Month Cash Flow Application",
    layout="wide"
)

def process_score_cashflow(uploaded_file):
    """
    Process SCORE cash flow template and convert it to the required format with
    Month, Cash Inflow, and Cash Outflow columns.
    """
    # Read the Excel file
    df = pd.read_excel(uploaded_file)
    
    # Extract months (excluding Pre-Startup EST and Total Item EST columns)
    months = [col for col in df.columns if col.endswith('-YY')]
    
    # Initialize lists to store data
    processed_data = []
    
    for month in months:
        # Cash Inflows (Cash Receipts)
        cash_inflow = df.loc[df.index[df['CASH RECEIPTS'].notna()].min():
                           df.index[df['TOTAL CASH RECEIPTS'].notna()].min()-1, 
                           month].sum()
        
        # Cash Outflows (Cash Paid Out)
        cash_outflow = df.loc[df.index[df['CASH PAID OUT'].notna()].min():
                            df.index[df['TOTAL CASH PAID OUT'].notna()].min()-1,
                            month].sum()
        
        # Store the processed data
        processed_data.append({
            'Month': month.replace('-YY', ''),
            'Cash Inflow': cash_inflow,
            'Cash Outflow': cash_outflow
        })
    
    # Convert to DataFrame
    result_df = pd.DataFrame(processed_data)
    
    return result_df

def main():
    st.title("12-Month Cash Flow Application")
    
    # Add instructions
    st.markdown("""
    ### Instructions:
    1. Upload your SCORE cash flow Excel file
    2. View the processed data and visualizations
    3. Download the processed results if needed
    """)
    
    # File upload
    uploaded_file = st.file_uploader("Upload your SCORE cash flow Excel file", 
                                   type=["xls", "xlsx"])
    
    if uploaded_file:
        try:
            # Process the SCORE template
            processed_data = process_score_cashflow(uploaded_file)
            
            # Display raw data
            st.subheader("Processed Data")
            st.dataframe(processed_data)
            
            # Summary metrics
            st.subheader("Summary Metrics")
            processed_data['Net Cash Flow'] = (processed_data['Cash Inflow'] - 
                                             processed_data['Cash Outflow'])
            
            # Create columns for metrics
            col1, col2, col3 = st.columns(3)
            
            total_inflow = processed_data['Cash Inflow'].sum()
            total_outflow = processed_data['Cash Outflow'].sum()
            net_flow = processed_data['Net Cash Flow'].sum()
            
            with col1:
                st.metric("Total Cash Inflow", f"${total_inflow:,.2f}")
            with col2:
                st.metric("Total Cash Outflow", f"${total_outflow:,.2f}")
            with col3:
                st.metric("Net Cash Flow", f"${net_flow:,.2f}")
            
            # Visualization
            st.subheader("Cash Flow Trend")
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Plot with better styling
            ax.plot(processed_data['Month'], processed_data['Cash Inflow'], 
                   label='Cash Inflow', marker='o', color='green', linewidth=2)
            ax.plot(processed_data['Month'], processed_data['Cash Outflow'], 
                   label='Cash Outflow', marker='o', color='red', linewidth=2)
            ax.plot(processed_data['Month'], processed_data['Net Cash Flow'], 
                   label='Net Cash Flow', marker='o', color='blue', linewidth=2)
            
            ax.set_xlabel("Month")
            ax.set_ylabel("Amount ($)")
            ax.set_title("Monthly Cash Flow")
            ax.legend()
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # Adjust layout to prevent label cutoff
            plt.tight_layout()
            
            st.pyplot(fig)
            
            # Download processed data
            st.download_button(
                label="Download Processed Data",
                data=processed_data.to_csv(index=False).encode('utf-8'),
                file_name="processed_cashflow.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.info("Please ensure you're uploading a valid SCORE cash flow template.")

if __name__ == "__main__":
    main()
