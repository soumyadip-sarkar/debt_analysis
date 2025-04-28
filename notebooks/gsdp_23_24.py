import pandas as pd

# Load the cleaned Excel file
df = pd.read_excel("../data/GDP_of_Indian_Statewise.xlsx")

# Create a new DataFrame with State and GDP 2023-24
df_csv = df[['State', '2023-24']].copy()

# Convert GDP from lakh crores to crores
df_csv['GDP 2023-24 (₹ crores)'] = (df_csv['2023-24'] * 100000).round(0).astype('Int64')

# Drop the original GDP column (in lakh crores)
df_csv.drop(columns=['2023-24'], inplace=True)

print(df_csv)
# Save to CSV
df_csv.to_csv("../data/state_gdp_2023_24.csv", index=False)
