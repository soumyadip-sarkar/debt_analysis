import pandas as pd
import sqlite3
import os

# File paths
csv_path_1 = "../data/public_sector_banks.csv"
csv_path_2 = "../data/private_sector_banks.csv"
csv_path_3 = "../data/foreign_banks.csv"
csv_path_4 = "../data/small_finance_banks.csv"

# Ensure 'database' directory exists
os.makedirs("../database", exist_ok=True)

# Connect to correct database path
conn = sqlite3.connect("../database/state_debt_bank.db")
cursor = conn.cursor()

# Correct CREATE TABLE queries (fixed typo INTEGER and table names)
create_table_queries = {
    "public_sector_banks": """
        CREATE TABLE IF NOT EXISTS public_sector_banks(
            State TEXT,
            Total_number_of_accounts INTEGER,
            Total_outstanding_Amount INTEGER,
            Small_borrower_accounts INTEGER,
            Small_borrower_outstanding_amount INTEGER
        )
    """,
    "private_sector_banks": """
        CREATE TABLE IF NOT EXISTS private_sector_banks(
            State TEXT,
            Total_number_of_accounts INTEGER,
            Total_outstanding_Amount INTEGER,
            Small_borrower_accounts INTEGER,
            Small_borrower_outstanding_amount INTEGER
        )
    """,
    "foreign_banks": """
        CREATE TABLE IF NOT EXISTS foreign_banks(
            State TEXT,
            Total_number_of_accounts INTEGER,
            Total_outstanding_Amount INTEGER,
            Small_borrower_accounts INTEGER,
            Small_borrower_outstanding_amount INTEGER
        )
    """,
    "small_finance_banks": """
        CREATE TABLE IF NOT EXISTS small_finance_banks(
            State TEXT,
            Total_number_of_accounts INTEGER,
            Total_outstanding_Amount INTEGER,
            Small_borrower_accounts INTEGER,
            Small_borrower_outstanding_amount INTEGER
        )
    """
}

# Execute table creation
for query in create_table_queries.values():
    cursor.execute(query)

# Load all CSV files
df1 = pd.read_csv(csv_path_1)
df2 = pd.read_csv(csv_path_2)
df3 = pd.read_csv(csv_path_3)
df4 = pd.read_csv(csv_path_4)

# Define insertion function
def insert_data(df, table_name):
    for _, row in df.iterrows():
        try:
            cursor.execute(f"""
                INSERT INTO {table_name} (State, Total_number_of_accounts, Total_outstanding_Amount, Small_borrower_accounts, Small_borrower_outstanding_amount)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row['State'],
                int(row['Total No. of Accounts']),
                int(row['Total Amount Outstanding ( ₹ Crores)']),
                int(row['SMALL BORROWERS No. of Accounts']),
                int(row['SMALL BORROWERS Amount Outstanding ( ₹ Crores)'])
            ))
        except Exception as e:
            print(f"Error inserting row for {row['State']} into {table_name}: {e}")

# Insert data into each table
insert_data(df1, "public_sector_banks")
insert_data(df2, "private_sector_banks")
insert_data(df3, "foreign_banks")
insert_data(df4, "small_finance_banks")

# Save and close the connection
conn.commit()
conn.close()

print(" Data successfully loaded into SQLite database.")
