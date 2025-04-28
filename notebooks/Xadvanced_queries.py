import sqlite3
import pandas as pd
import os

# Connect to your database
db_path = os.path.join("..", "database", "debt_allocation.db")
conn = sqlite3.connect(db_path)

# Number of Cities per State
query_cities_per_state = """
SELECT State, COUNT(City) AS Number_of_Cities
FROM debt_allocation
GROUP BY State
ORDER BY Number_of_Cities DESC;
"""
df_cities_per_state = pd.read_sql_query(query_cities_per_state, conn)
print("\n Number of Cities per State:")
print(df_cities_per_state)

# Average Borrowing per State
query_avg_borrowing = """
SELECT State, AVG(City_Borrowing_Money) AS Average_Borrowing
FROM debt_allocation
GROUP BY State
ORDER BY Average_Borrowing DESC;
"""
df_avg_borrowing = pd.read_sql_query(query_avg_borrowing, conn)
print("\n Average Borrowing per State:")
print(df_avg_borrowing)

# Cities with Borrowing above ₹50,000 crore
query_high_borrowing = """
SELECT City, State, City_Borrowing_Money
FROM debt_allocation
WHERE City_Borrowing_Money > 100000000000
ORDER BY City_Borrowing_Money DESC;
"""
df_high_borrowing = pd.read_sql_query(query_high_borrowing, conn)
print("\n Cities with Borrowing above ₹10,000 crore:")
print(df_high_borrowing)

# State with Highest Single-City Borrowing
query_max_city = """
SELECT City, State, MAX(City_Borrowing_Money) AS Max_Borrowing
FROM debt_allocation
ORDER BY Max_Borrowing DESC
LIMIT 1;
"""
df_max_city = pd.read_sql_query(query_max_city, conn)
print("\n City with Highest Borrowing:")
print(df_max_city)

# Total Borrowing in India
query_total_borrowing = """
SELECT SUM(City_Borrowing_Money) AS Total_India_Borrowing
FROM debt_allocation;
"""
df_total_borrowing = pd.read_sql_query(query_total_borrowing, conn)
print("\n Total Borrowing in India:")
print(df_total_borrowing)

# Close connection
conn.close()

# Directory to save CSVs
output_dir = os.path.join("..", "data")
os.makedirs(output_dir, exist_ok=True)

# Save each query result as CSV
df_cities_per_state.to_csv(os.path.join(output_dir, "cities_per_state.csv"), index=False)
df_avg_borrowing.to_csv(os.path.join(output_dir, "avg_borrowing_per_state.csv"), index=False)
df_high_borrowing.to_csv(os.path.join(output_dir, "high_borrowing_cities.csv"), index=False)
df_max_city.to_csv(os.path.join(output_dir, "highest_single_city_borrowing.csv"), index=False)
df_total_borrowing.to_csv(os.path.join(output_dir, "total_india_borrowing.csv"), index=False)
