import sqlite3
import pandas as pd
import os

# Connect to your database
db_path = os.path.join("..", "database", "debt_allocation.db")
conn = sqlite3.connect(db_path)

# Query 1: View all data
query_all = "SELECT * FROM debt_allocation"
df_all = pd.read_sql_query(query_all, conn)
print("\nAll records:")
print(df_all.head())

# Query 2: Top 10 cities with highest borrowing amount
query_top_10 = """
SELECT City, State, City_Borrowing_Money
FROM debt_allocation
ORDER BY City_Borrowing_Money DESC
LIMIT 10
"""
df_top_10 = pd.read_sql_query(query_top_10, conn)
print("\nTop 10 cities by borrowing amount:")
print(df_top_10)

# Query 3: Total debt by state
query_total_by_state = """
SELECT State, SUM(City_Borrowing_Money) as Total_Borrowing
FROM debt_allocation
GROUP BY State
ORDER BY Total_Borrowing DESC
"""
df_total_by_state = pd.read_sql_query(query_total_by_state, conn)
print("\nTotal debt by state:")
print(df_total_by_state)

# Close connection
conn.close()
