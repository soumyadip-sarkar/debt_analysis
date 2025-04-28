import pandas as pd
import os

# file path (as string)
file_path = r"C:\Users\Soumyadip\Desktop\city_population_debt_analysis\data\state_debt_data_rbi.xlsx"
sheet_name = "Report 1"

# Output directory
output_dir = r"C:\Users\Soumyadip\Desktop\city_population_debt_analysis\data"
os.makedirs(output_dir, exist_ok=True)

# Load Excel file
print(" Reading Excel file")
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Clean header row
df.columns = df.iloc[0]   # Set first row as header
df = df[1:]               # Drop header row
df.rename(columns={df.columns[0]: "Bank Group"}, inplace=True)

# Replace '&' with 'and' in all string cells
df = df.applymap(lambda x: x.replace("&", "and") if isinstance(x, str) else x)

# Define bank groups and output filenames
bank_groups = {
    "PUBLIC SECTOR BANKS": "public_sector_banks.csv",
    "PRIVATE SECTOR BANKS": "private_sector_banks.csv",
    "FOREIGN BANKS": "foreign_banks.csv",
    "SMALL FINANCE BANKS": "small_finance_banks.csv",
    "ALL SCHEDULED COMMERCIAL BANKS": "all_scheduled_commercial_banks.csv"
}

# Filter and save each group
for group, filename in bank_groups.items():
    filtered_df = df[df["Bank Group"] == group]
    output_path = os.path.join(output_dir, filename)
    filtered_df.to_csv(output_path, index=False)
    print(f"Saved {group} data to {output_path}")

print("\n All CSV files created successfully!")



