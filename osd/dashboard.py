import streamlit as st
import pandas as pd
from django_pandas.io import read_frame
from osd.models import validation  # Adjust the import according to your app structure

# Fetch data from Django model
def fetch_data(start_date=None, end_date=None):
    data = validation.objects.all()
    df = read_frame(data)

    if start_date and end_date:
        df = df[(df['deduction_date'] >= start_date) & (df['deduction_date'] <= end_date)]

    return df

def main():
    st.title("Validation Dashboard")

    # Load data
    df = fetch_data()

    # Check if DataFrame is empty
    if not df.empty:
        # Get min and max dates from the data
        min_date = df['deduction_date'].min()
        max_date = df['deduction_date'].max()

        # Sidebar filters
        st.sidebar.header('Filters')
        start_date = st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
        end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

        # Filter data based on selected date range
        df = fetch_data(start_date, end_date)
        
        # Display data
        st.subheader('Filtered Data')
        st.write(df)

        # Display totals
        if not df.empty:
            total_deductions = df.shape[0]
            total_invalid = df[df['validation_status'] == 'invalid'].shape[0]
            total_valid = df[df['validation_status'] == 'valid'].shape[0]

            st.subheader('Totals')
            st.write(f'Total Deductions: {total_deductions}')
            st.write(f'Total Invalid: {total_invalid}')
            st.write(f'Total Valid: {total_valid}')
        else:
            st.write('No data available for the selected date range.')
    else:
        st.write('No data available.')

if __name__ == "__main__":
    main()
