import pandas as pd
import os

# Paths to your data files
all_cities_path = os.path.join("data", "cleaned", "all_indian_cities_population_cleaned.csv")
tier2_cities_path = os.path.join("data", "tier2_cities.csv")
output_path = os.path.join("data", "city_categories.csv")

# Load the all cities data
all_cities_df = pd.read_csv(all_cities_path)

# Load the Tier-2 cities list
tier2_df = pd.read_csv(tier2_cities_path)

# Clean Tier-2 city names (remove junk like 'and', '.', empty strings)
tier2_df = tier2_df[~tier2_df['City'].isin(['and', '.', ''])]
tier2_cities = tier2_df['City'].unique().tolist()

# Define Tier-1 cities manually (as per your corrected list)
tier1_cities = [
    'Ahmedabad', 'Bengaluru', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Pune'
]

# Function to assign category
def assign_category(city):
    if city in tier1_cities:
        return 'Tier-1'
    elif city in tier2_cities:
        return 'Tier-2'
    else:
        return 'Tier-3'

# Apply categorization
all_cities_df['Category'] = all_cities_df['City'].apply(assign_category)

# Create final DataFrame with only City and Category
final_df = all_cities_df[['City', 'Category']]

# Save to CSV
final_df.to_csv(output_path, index=False)

print(f"City categorization completed. Saved to {output_path}")
