import pandas as pd

# Load your CSV file into a DataFrame
df = pd.read_csv(r'C:\Users\703188067\Desktop\validation_engine\sample data\osd_invoice..csv')

# Concatenate invoice_number, deduction_date, and deduction_amount to create a unique identifier
df['unique_key'] = df['invoice_number'].astype(str) + df['sku'].astype(str) + df['billed_qty'].astype(str)

# Drop duplicates based on the unique_key column
df_unique = df.drop_duplicates(subset=['unique_key'])

# Drop the unique_key column if you don't want it in the output
df_unique = df_unique.drop(columns=['unique_key'])

# Save the cleaned data to a new CSV file
df_unique.to_csv('cleaned_file.csv', index=False)

print("Duplicates removed and new file saved as cleaned_file.csv")
