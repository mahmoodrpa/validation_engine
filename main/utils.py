import zipfile
from django.conf import settings
import re
import pandas as pd
import os
from datetime import datetime
from django.db.models import Sum, F, Value
from django.db.models import Q
from decimal import Decimal

# def convert_to_decimal(value):
#     if isinstance(value, str):
#         try:
#             return float(value.replace(',', ''))
#         except ValueError:
#             return None
#     elif isinstance(value, float):
#         return value
#     else:
#         return None


def convert_to_decimal(value):
    if value is None or value == '':
        return 0.0
    
    if isinstance(value, str):
        # Normalize the string: strip whitespace, replace commas, and handle "nan"
        value = value.strip().replace(',', '').lower()
        if value == 'nan':
            return 0.0
        # Use regex to detect if the string can be converted to a number
        if re.match(r'^-?\d+(\.\d+)?$', value):
            try:
                return float(value)
            except ValueError:
                return None
        else:
            return None
    elif isinstance(value, (float, int)):
        return float(value)
    else:
        return None


def validate_and_convert(data):
    try:
        return convert_to_decimal(data)
    except ValueError:
        return 0.0


def convert_to_decimal_V2(value):    
    if isinstance(value, str):
        try:
            # Remove dollar signs and commas, then convert to float
            cleaned_value = value.replace('$', '').replace(',', '')
            result = float(cleaned_value)
            return result
        except ValueError:
            return None
    elif isinstance(value, (int, float)):
        return float(value)
    else:
        # return None
        return  0.0


def convert_to_decimal_V3(value):    
    if isinstance(value, str):
        try:
            # Remove dollar signs and commas, then convert to float
            cleaned_value = value.replace('$', '').replace(',', '').replace('CAD', '')
            result = float(cleaned_value)
            return result
        except ValueError:
            return None
    elif isinstance(value, (int, float)):
        return float(value)
    else:
        # return None
        return  0.0


def read_file_from_zip(zip_path, selected_file):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            with zip_ref.open(selected_file) as file:
                if selected_file.endswith('.csv'):
                    df = pd.read_csv(file)
                elif selected_file.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file)
                   
                else:
                    raise ValueError("Unsupported file type. Please select a CSV or Excel file.")
                return df
    except Exception as e:
        print(f"An error occurred while reading the file from ZIP archive: {e}")
        return None

def get_folder_path(user_directory_path, file_name):
    # This is a placeholder function, implement it based on your directory structure
    for root, dirs, files in os.walk(user_directory_path):
        if file_name in files:
            return root
    return None

def parse_date(date_str):
    if pd.isnull(date_str):
        return None
    if not isinstance(date_str, str):
        date_str = str(date_str).strip()
    else:
        date_str = date_str.strip()

    date_formats = [
        '%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d-%b-%y', '%d-%b-%Y',
        '%m/%d/%y', '%Y/%m/%d', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%d %H:%M:%S', '%d-%m-%y', '%m-%d-%y'
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    print(f"Error parsing date: {date_str}")
    return None



def extract_rebate_prct(description):
    match = re.search(r'-\s*([\d.]+)\s*%', description)
    if match:
        # print(f"Found rebate percentage: {match.group(1)}")  # Debugging statement
        return float(match.group(1))
    else:
        # print(f"Rebate percentage not found in description: {description}")  # Debugging statement
        return None



def extract_agreement_end(description):
    match = re.search(r'Cost Price based on Net Receipts Period \d{4}/\d{2}/\d{2} to (\d{4}/\d{2}/\d{2})', description)
    return parse_date(match.group(1)) if match else None


def clean_value(value, default=0.0):
                if pd.isna(value) or value in ['#DIV/0!', '']:
                    return default
                try:
                    return float(value)
                except ValueError:
                    return default

def clean_value_v2(value, default):
    return value if value is not None and value != '' else default    

def clean_value_v3(value, default):
    # Check if the value is NaN or empty
    if pd.isna(value) or value == '':
        return default
    return value                    

def calculate_total_deductions(queryset):
    # Sum of Deduction amount
    total_deductions = queryset.aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0

    # Count the number of rows in the queryset
    num_rows = queryset.count()
    # Round off the result to two decimal places
    total_deductions = round(total_deductions, 2)

    return total_deductions , num_rows

def calculate_total_invalid(queryset):
    # Sum of INVALID AMOUNT
    total_invalid = queryset.aggregate(Sum('invalid_amt'))['invalid_amt__sum'] or 0

    # Count the number of rows in the queryset
    # invalid_rows = queryset.count()
    invalid_rows = queryset.filter(Q(validation_status="Invalid") | Q(validation_status="Partially Invalid")).count()

    # Round off the result to two decimal places
    total_invalid = round(total_invalid, 2)

    return total_invalid ,invalid_rows

def calculate_total_valid(queryset):
    # Total Deductions - Total Invalid
    total_deductions, _ = calculate_total_deductions(queryset)
    total_invalid, _ = calculate_total_invalid(queryset)

    # Count the number of valid rows in the queryset
    valid_rows = queryset.filter(validation_status="Valid").count()

    # Round off the result to two decimal places
    total_valid = round(total_deductions - total_invalid, 2)

    return total_valid , valid_rows

  

from decimal import Decimal

def calculate_rca_split(queryset):
    # Initialize sum variables for each reason
    load_wise_sum = Decimal('0.0')
    duplicate_sum = Decimal('0.0')
    rate_wise_sum = Decimal('0.0')
    edi_mismatch_sum = Decimal('0.0')

    # Iterate through the queryset and accumulate sums for each reason
    for item in queryset:
        final_rca = item.final_rca
        invalid_amt = item.invalid_amt if item.invalid_amt is not None else Decimal('0.0')

        if final_rca and 'Freight is already given on the invoice' in final_rca:
            load_wise_sum += invalid_amt
        elif final_rca and 'Duplicate Freight Deduction' in final_rca:
            duplicate_sum += invalid_amt
        elif final_rca and 'Freight is taken at a higher rate than communicated' in final_rca:
            rate_wise_sum += invalid_amt
        elif final_rca and 'EDI Mismatch' in final_rca:
            edi_mismatch_sum += invalid_amt

    # Convert Decimal sums to float before constructing the dictionary
    sums = {
        'load_wise_sum': float(load_wise_sum),
        'duplicate_sum': float(duplicate_sum),
        'rate_wise_sum': float(rate_wise_sum),
        'edi_mismatch_sum': float(edi_mismatch_sum),
    }

    return sums


