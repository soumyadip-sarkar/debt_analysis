import pandas as pd

# Step 1: Load the CSV files
debt_df = pd.read_csv("../data/all_scheduled_commercial_banks.csv")
gdp_df = pd.read_csv("../data/state_gdp_2023_24.csv")

# Step 2: Check the actual column names
print("Debt DataFrame columns:", debt_df.columns.tolist())
print("GDP DataFrame columns:", gdp_df.columns.tolist())

# Step 3: Rename the columns for consistency
debt_df.rename(columns={
    debt_df.columns[1]: "State",
    debt_df.columns[3]: "Total Outstanding"
}, inplace=True)

gdp_df.rename(columns={
    gdp_df.columns[0]: "State",
    gdp_df.columns[1]: "GDP 2023-24"
}, inplace=True)

# Step 4: Clean state names (remove spaces and replace '&' with 'and')
debt_df["State"] = debt_df["State"].astype(str).str.strip().str.replace("&", "and")
gdp_df["State"] = gdp_df["State"].astype(str).str.strip().str.replace("&", "and")

# Step 5: Check if all states match
debt_states = set(debt_df["State"])
gdp_states = set(gdp_df["State"])
print("States in debt data but not in GDP:", debt_states - gdp_states)
print("States in GDP but not in debt data:", gdp_states - debt_states)

# Step 6: Merge both DataFrames on 'State'
merged_df = pd.merge(debt_df, gdp_df, on="State", how="inner")

# Step 7: Calculate Debt to GDP Ratio (%)
merged_df["Debt to GDP Ratio (%)"] = (merged_df["Total Outstanding"] / merged_df["GDP 2023-24"]) * 100
merged_df["Debt to GDP Ratio (%)"] = merged_df["Debt to GDP Ratio (%)"].round(2)

# Step 8: Rename columns for clarity
merged_df.rename(columns={
    "Total Outstanding": "Total Amount Outstanding (₹ Crores)",
    "GDP 2023-24": "GDP 2023-24 (₹ Crores)"
}, inplace=True)

# Step 9: Save to new CSV
final_df = merged_df[["State", "Total Amount Outstanding (₹ Crores)", "GDP 2023-24 (₹ Crores)", "Debt to GDP Ratio (%)"]]
final_df.to_csv("../data/debt_to_gdp_final.csv", index=False)

print("debt_to_gdp_final.csv has been created successfully!")
