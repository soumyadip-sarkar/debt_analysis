import sqlite3
import pandas as pd
import os

# Define paths
data_folder = r'C:\Users\Soumyadip\Desktop\city_population_debt_analysis\data'
db_path = r'C:\Users\Soumyadip\Desktop\city_population_debt_analysis\database\debt_allocation_details.db'

# CSV files and corresponding table names
csv_files = {
    'all_indian_cities_population_cleaned.csv': 'city_population',
    'city_categories.csv': 'city_categories',
    'debt_allocation_to_cities.csv': 'city_debt'
}

# Connect to SQLite database (will create if not exists)
conn = sqlite3.connect(db_path)

# Loop over CSV files and insert into database
for filename, table_name in csv_files.items():
    file_path = os.path.join(data_folder, filename)
    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f" Loaded {filename} into table `{table_name}`")

# Optional: Check a few rows from each table
for table_name in csv_files.values():
    print(f"\nPreview of `{table_name}` table:")
    print(pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5;", conn))

# Close connection
conn.close()
