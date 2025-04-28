import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

print("Setup working fine! ✅")

print("Current Working Directory:", os.getcwd())

import pandas as pd
import sqlite3
import os

csv_path = "../data/debt_allocation_to_cities.csv"

if not os.path.exists(csv_path):
    print(f"CSV file not found at {csv_path}. Please check the path.")
    exit()

df = pd.read_csv(csv_path)
print("Sample data:")
print(df.head())

# ✅ Ensure 'database' directory exists
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/debt_allocation.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS debt_allocation")

create_table_query = """
CREATE TABLE debt_allocation (
    City TEXT,
    State TEXT,
    City_Outstanding_Amount INTEGER
)
"""
cursor.execute(create_table_query)

for _, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO debt_allocation (City, State, City_Outstanding_Amount)
            VALUES (?, ?, ?)
        """, (row['City'], row['State'], int(row['City Total Amount Outstanding ( ₹ Crores)'])))
    except Exception as e:
        print(f"Error inserting row {row['City']}, {row['State']}: {e}")

conn.commit()
conn.close()

print("Data successfully loaded into SQLite database.")
