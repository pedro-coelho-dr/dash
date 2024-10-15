import os
import pandas as pd
from db_handler import add_transaction, add_category, get_all_categories

# Define the CSV file path
csv_file_path = os.path.join(os.path.dirname(__file__), 'seed.csv')

# Read the CSV file, ensuring proper column parsing and separator handling
df = pd.read_csv(csv_file_path, sep=',', header=0)

# Check if the 'date' column contains valid date values
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')  # 'coerce' will turn invalid dates into NaT (missing dates)

# Print out the rows where dates are NaT to debug
print("Rows with invalid or missing dates:")
print(df[df['date'].isna()])

# Seed script to insert categories and transactions from CSV file
def seed_database_from_csv():
    # Check if categories already exist in the database
    existing_categories = set(get_all_categories())

    # Loop over each row in the DataFrame to add the transaction
    for index, row in df.iterrows():
        # Handle categories for each transaction (splitting on commas)
        categories = row['categories'].split(', ') if pd.notna(row['categories']) else []
        
        # Add new categories if not already in the database
        for category in categories:
            if category not in existing_categories:
                add_category(category)
                existing_categories.add(category)

        # Debug output for each transaction
        print(f"Processing transaction {index+1}: Date = {row['date']}, Type = {row['type']}, Description = {row['description']}")
        
        # Add the transaction if the date is valid
        if pd.notna(row['date']):
            add_transaction(
                date=row['date'],
                type_=row['type'],  # Crédito or Débito
                description=row['description'],
                payment_method=row['payment_method'],
                bank=row['bank'],
                value=row['value'],
                categories=categories,
                notes=row['notes'] if pd.notna(row['notes']) else ''
            )
        else:
            print(f"Skipping transaction {index+1} due to invalid date.")

    print("Database successfully seeded with transactions from CSV.")

# Run the seed function
if __name__ == "__main__":
    seed_database_from_csv()
