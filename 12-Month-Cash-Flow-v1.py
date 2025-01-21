import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit app
def main():
    st.title("12-Month Cash Flow Application")

    # File upload
    uploaded_file = st.file_uploader("Upload your 12-month cash flow Excel file", type=["xls", "xlsx"])

    if uploaded_file:
        # Load the Excel file
        try:
            data = pd.read_excel(uploaded_file)
            
            # Display raw data
            st.subheader("Uploaded Data")
            st.dataframe(data)

            # Summary metrics
            st.subheader("Summary Metrics")
            if {'Month', 'Cash Inflow', 'Cash Outflow'}.issubset(data.columns):
                data['Net Cash Flow'] = data['Cash Inflow'] - data['Cash Outflow']

                total_inflow = data['Cash Inflow'].sum()
                total_outflow = data['Cash Outflow'].sum()
                net_flow = data['Net Cash Flow'].sum()

                st.write(f"**Total Cash Inflow:** ${total_inflow:,.2f}")
                st.write(f"**Total Cash Outflow:** ${total_outflow:,.2f}")
                st.write(f"**Net Cash Flow:** ${net_flow:,.2f}")

                # Visualization
                st.subheader("Cash Flow Trend")
                fig, ax = plt.subplots()
                ax.plot(data['Month'], data['Cash Inflow'], label='Cash Inflow', marker='o')
                ax.plot(data['Month'], data['Cash Outflow'], label='Cash Outflow', marker='o')
                ax.plot(data['Month'], data['Net Cash Flow'], label='Net Cash Flow', marker='o')
                
                ax.set_xlabel("Month")
                ax.set_ylabel("Amount ($)")
                ax.set_title("Monthly Cash Flow")
                ax.legend()
                plt.xticks(rotation=45)

                st.pyplot(fig)
            else:
                st.error("The uploaded file must contain 'Month', 'Cash Inflow', and 'Cash Outflow' columns.")

        except Exception as e:
            st.error(f"Error loading file: {e}")

if __name__ == "__main__":
    main()
