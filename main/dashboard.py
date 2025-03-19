import streamlit as st
import pandas as pd
from django_pandas.io import read_frame

from osd.models import validation  # Adjust the import according to your app structure

# Fetch data from Django model
def fetch_data():
    data = validation.objects.all().values()
    df = pd.DataFrame(list(data))
    return df

def main():
    st.title("Validation Dashboard")

    # Load data
    df = fetch_data()

    # Sidebar filters
    st.sidebar.header('Filters')
    start_date = st.sidebar.date_input("Start Date", min_value=df['deduction_date'].min())
    end_date = st.sidebar.date_input("End Date", max_value=df['deduction_date'].max())
    
    filtered_data = df[(df['deduction_date'] >= start_date) & (df['deduction_date'] <= end_date)]

    # Display data
    st.subheader('Filtered Data')
    st.write(filtered_data)

    # Display totals
    total_deductions = filtered_data.shape[0]
    total_invalid = filtered_data[filtered_data['validation_status'] == 'invalid'].shape[0]
    total_valid = filtered_data[filtered_data['validation_status'] == 'valid'].shape[0]
    
    st.subheader('Totals')
    st.write(f'Total Deductions: {total_deductions}')
    st.write(f'Total Invalid: {total_invalid}')
    st.write(f'Total Valid: {total_valid}')

if __name__ == "__main__":
    main()
