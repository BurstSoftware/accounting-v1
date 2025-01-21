import pandas as pd
import numpy as np

def process_score_cashflow(file_path):
    """
    Process SCORE cash flow template and convert it to the required format with
    Month, Cash Inflow, and Cash Outflow columns.
    """
    # Read the Excel file
    df = pd.read_excel(file_path)
    
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

def export_processed_data(input_file, output_file):
    """
    Process the SCORE cash flow template and export to a new Excel file
    in the required format.
    """
    processed_df = process_score_cashflow(input_file)
    processed_df.to_excel(output_file, index=False)
    return processed_df

# Modified Streamlit app code
def main():
    st.title("12-Month Cash Flow Application")
    
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
            
            total_inflow = processed_data['Cash Inflow'].sum()
            total_outflow = processed_data['Cash Outflow'].sum()
            net_flow = processed_data['Net Cash Flow'].sum()
            
            st.write(f"**Total Cash Inflow:** ${total_inflow:,.2f}")
            st.write(f"**Total Cash Outflow:** ${total_outflow:,.2f}")
            st.write(f"**Net Cash Flow:** ${net_flow:,.2f}")
            
            # Visualization
            st.subheader("Cash Flow Trend")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(processed_data['Month'], processed_data['Cash Inflow'], 
                   label='Cash Inflow', marker='o', color='green')
            ax.plot(processed_data['Month'], processed_data['Cash Outflow'], 
                   label='Cash Outflow', marker='o', color='red')
            ax.plot(processed_data['Month'], processed_data['Net Cash Flow'], 
                   label='Net Cash Flow', marker='o', color='blue')
            
            ax.set_xlabel("Month")
            ax.set_ylabel("Amount ($)")
            ax.set_title("Monthly Cash Flow")
            ax.legend()
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig)
            
            # Download processed data
            st.download_button(
                label="Download Processed Data",
                data=processed_data.to_csv(index=False),
                file_name="processed_cashflow.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"Error processing file: {e}")

if __name__ == "__main__":
    main()
