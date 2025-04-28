import pandas as pd
import os

# Load city population and working population data
city_df = pd.read_csv("data/cleaned/all_indian_cities_population_cleaned.csv")

# Check required columns exist
required_columns = ['City', 'State', 'Working Population (2024 Estimate)']
for col in required_columns:
    if col not in city_df.columns:
        raise ValueError(f"Missing column in city data: {col}")

# Load state debt data
debt_df = pd.read_csv("data/all_scheduled_commercial_banks.csv")

# Check required columns exist
if 'State' not in debt_df.columns or 'Total Amount Outstanding ( ₹ Crores)' not in debt_df.columns:
    raise ValueError("Missing 'State' or 'Total Amount Outstanding ( ₹ Crores)' column in debt data.")

# Initialize list to collect allocation data
allocation_data = []

# Process each state
for _, state_row in debt_df.iterrows():
    state_name = state_row['State']
    number_of_accounts = state_row['Total No. of Accounts']
    total_borrowing = state_row['Total Amount Outstanding ( ₹ Crores)']
    

    # Filter cities for the current state
    state_cities = city_df[city_df['State'] == state_name].copy()

    # Skip if no cities found for this state
    if state_cities.empty:
        continue

    # Total working population for this state
    total_working_pop = state_cities['Working Population (2024 Estimate)'].sum()

    # Skip if working population is zero to avoid division by zero
    if total_working_pop == 0:
        continue
    
    # Allocate number of loan accounts proportionally and round to nearest integer
    state_cities['Number of Loan Accounts'] = (
        (state_cities['Working Population (2024 Estimate)'] / total_working_pop) * number_of_accounts
    ).round(0).astype('Int64')

    # Allocate borrowing amount proportionally and round to nearest integer
    state_cities['City Total Amount Outstanding ( ₹ Crores)'] = (
        (state_cities['Working Population (2024 Estimate)'] / total_working_pop) * total_borrowing
    ).round(0).astype('Int64')

    
    # Select required columns
    allocation_data.append(state_cities[['City', 'State', 'City Total Amount Outstanding ( ₹ Crores)','Number of Loan Accounts']])

# Concatenate all allocations
final_df = pd.concat(allocation_data, ignore_index=True)

# Sort by borrowing money in descending order
final_df.sort_values(by='City Total Amount Outstanding ( ₹ Crores)', ascending=False, inplace=True)

# Save to CSV
os.makedirs("data/cleaned", exist_ok=True)
final_df.to_csv("data/cleaned/debt_allocation_to_cities.csv", index=False)

# Preview result
print(" Debt allocation completed. Preview:")
print(final_df.head(20))
