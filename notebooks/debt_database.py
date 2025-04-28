import pandas as pd
import sqlite3
import os

# Correct file paths
csv_path_1 = "../data/debt_allocation_to_cities.csv"
csv_path_2 = "../data/city_categories.csv"
csv_path_3 = "../data/all_indian_cities_population_cleaned.csv"

#  Ensure 'database' directory exists
os.makedirs("database", exist_ok=True)

#  Connect to correct database path
conn = sqlite3.connect("../database/debt_analysis.db")
cursor = conn.cursor()

#  Create first table: city_debt
create_table_query_1 = """
CREATE TABLE IF NOT EXISTS city_debt(
    City TEXT,
    State TEXT,
    City_Outstanding_Amount INTEGER,
    City_Loan_Accounts INTEGER
)
"""
cursor.execute(create_table_query_1)

#  Load and insert data into city_debt
df1 = pd.read_csv(csv_path_1)

for _, row in df1.iterrows():
    try:
        cursor.execute("""
            INSERT INTO city_debt (City, State, City_Outstanding_Amount, City_Loan_Accounts)
            VALUES (?, ?, ?, ?)
        """, (row['City'], row['State'], int(row['City Total Amount Outstanding ( ₹ Crores)']), int(row['Number of Loan Accounts'])))
    except Exception as e:
        print(f"Error inserting row {row['City']}, {row['State']}: {e}")

#  Create second table: city_categories
create_table_query_2 = """
CREATE TABLE IF NOT EXISTS city_categories(
    City TEXT,
    Category TEXT
)
"""
cursor.execute(create_table_query_2)

#  Load and insert data into city_categories
df2 = pd.read_csv(csv_path_2)

for _, row in df2.iterrows():
    try:
        cursor.execute("""
            INSERT INTO city_categories (City, Category)
            VALUES (?, ?)
        """, (row['City'], row['Category']))
    except Exception as e:
        print(f"Error inserting row {row['City']}: {e}")

#  Create third table: city_population
create_table_query_3 = """
CREATE TABLE IF NOT EXISTS city_population(
    City TEXT,
    State TEXT,
    City_population INTEGER,
    Working_population INTEGER
)
"""
cursor.execute(create_table_query_3)

#  Load and insert data into city_population
df3 = pd.read_csv(csv_path_3)

for _, row in df3.iterrows():
    try:
        cursor.execute("""
            INSERT INTO city_population (City, State, City_population, Working_population)
            VALUES (?, ?, ?, ?)
        """, (row['City'], row['State'], int(row['Population (2024 Estimate)']), int(row['Working Population (2024 Estimate)'])))
    except Exception as e:
        print(f"Error inserting row {row['City']}, {row['State']}: {e}")

# Save and close the connection
conn.commit()
conn.close()

print("Data successfully loaded into SQLite database.")
